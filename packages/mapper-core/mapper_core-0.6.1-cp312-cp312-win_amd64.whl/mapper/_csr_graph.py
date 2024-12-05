# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++
"""Functions that work with the underlying CSR graph structures."""

from typing import List, Tuple, Union

import cython
import numpy as np
from cython.cimports.libc.math import fabs
from cython.cimports.libc.stdint import int32_t, int64_t
from cython.cimports.libcpp.vector import vector

# used for functions like the filter pruning ones that might be called with
# float or integer values.
numeric = cython.fused_type(cython.float, cython.double, int32_t, int64_t)
bool_like = cython.fused_type(cython.char, cython.integral)


## Conversion to other formats


@cython.boundscheck(False)
@cython.wraparound(False)
def get_edge_list_masked_csr(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    edge_ranks: int32_t[:],
    mask: cython.char[:],
    max_rank: cython.int,
) -> List[Tuple[int, int]]:
    """Returns a list of tuples giving the edges of the (undirected) graph.

    Only includes an edge (i,j) if j is a neighbor of i of rank <= max_rank, and
    the corresponding entry in mask is True.  Assumes the graph is undirected,
    so only includes edges with i < j. The mask array must be symmetric, i.e.,
    if i->j is represented by index jdx, and j->i is represented by index idx,
    mask[jdx] is True if and only if mask[idx] is True.
    """
    edge_list = []
    N: cython.Py_ssize_t = len(neighborhood_boundaries) - 1
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: int32_t
    for i in range(N):
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            if i < j and mask[jdx] and edge_ranks[jdx] < max_rank:
                edge_list.append((i, j))
    return edge_list


@cython.boundscheck(False)
@cython.wraparound(False)
def get_edge_list_masked_csr_no_rank(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    mask: cython.char[:],
) -> List[Tuple[int, int]]:
    """Returns a list of tuples giving the edges of the (undirected) graph.

    Only includes an edge (i,j) if j is a neighbor of i and the corresponding
    entry in mask is True.  Assumes the graph is undirected, so only includes
    edges with i < j. The mask array must be symmetric, i.e., if i->j is
    represented by index jdx, and j->i is represented by index idx, mask[jdx] is
    True if and only if mask[idx] is True.
    """
    edge_list = []
    N: cython.Py_ssize_t = len(neighborhood_boundaries) - 1
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: int32_t
    for i in range(N):
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            if i < j and mask[jdx]:
                edge_list.append((i, j))
    return edge_list


## Pruning edges based on filter values


@cython.boundscheck(False)
@cython.wraparound(False)
def prune_filter_mask_csr(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    f: numeric[::1],
    threshold: cython.float,
) -> np.ndarray:
    """Returns a boolean mask whose value on an edge is true if the difference
    in filter values |f(i) - f(j)| is <= threshold."""
    mask = np.zeros_like(neighbors, dtype=np.bool_)
    mask_view = cython.declare(cython.char[::1], mask)
    N: cython.Py_ssize_t = len(neighborhood_boundaries) - 1
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: int32_t
    for i in range(N):
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            filter_diff = fabs(f[i] - f[j])
            if filter_diff <= threshold:
                mask_view[jdx] = 1
    return mask


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cfunc
@cython.exceptval(check=False)
def in_sorted(x: int32_t, u: int32_t[::1]) -> cython.char:
    """Check whether x is in the sorted array u.

    Uses a simple bisecting search."""
    # This may be faster to implement using np.searchsorted(), but my naive
    # attempts actually slowed it down
    n_elts: cython.Py_ssize_t = len(u)
    if n_elts == 0:
        return 0
    bot_ix: cython.Py_ssize_t = 0
    top_ix: cython.Py_ssize_t = n_elts - 1
    mid_ix: cython.Py_ssize_t = n_elts - 1
    if x < u[bot_ix]:
        return 0
    if x > u[top_ix]:
        return 0
    while True:
        mid_ix = (bot_ix + top_ix) // 2
        if x < u[mid_ix]:
            top_ix = mid_ix
        elif x > u[mid_ix]:
            bot_ix = mid_ix
        else:
            return 1
        if top_ix - bot_ix <= 1:
            if x == u[top_ix] or x == u[bot_ix]:
                return 1
            else:
                return 0


@cython.boundscheck(False)
@cython.wraparound(False)
def prune_filter_mask_csr_local(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    f: numeric[::1],
    threshold: cython.float,
    domain: int32_t[::1],
) -> np.ndarray:
    """Returns a boolean mask whose value on an edge is false if the edge lies
    inside the domain and the difference in filter values |f(i) - f(j)| is >
    threshold."""
    mask = np.zeros_like(neighbors, dtype=np.bool_)
    mask_view = cython.declare(cython.char[::1], mask)
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: int32_t

    for i in domain:
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            if in_sorted(j, domain):
                filter_diff = fabs(f[i] - f[j])
                if filter_diff > threshold:
                    mask_view[jdx] = 1
    return mask


@cython.boundscheck(False)
@cython.wraparound(False)
def prune_filter_mask_csr_frac(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    filter_vals: numeric[::1],
    domain_partition: int32_t[::1],
    lower_bounds: numeric[::1],
    upper_bounds: numeric[::1],
) -> np.ndarray:
    mask = np.zeros_like(neighbors, dtype=np.bool_)
    mask_view = cython.declare(cython.char[::1], mask)
    N: cython.Py_ssize_t = len(neighborhood_boundaries) - 1
    i: cython.Py_ssize_t
    jdx: cython.Py_ssize_t
    j: int32_t
    i_partition: int32_t
    j_partition: int32_t
    f_i: numeric
    f_j: numeric

    for i in range(N):
        i_partition = domain_partition[i]
        f_i = filter_vals[i]
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            j_partition = domain_partition[j]
            f_j = filter_vals[j]
            if i_partition == j_partition:
                mask_view[jdx] = True
            elif i_partition == j_partition + 1:
                if f_j > lower_bounds[i_partition] and f_i < upper_bounds[j_partition]:
                    mask_view[jdx] = True
            elif i_partition == j_partition - 1:  # noqa: SIM102 for parallelism
                if f_i > lower_bounds[j_partition] and f_j < upper_bounds[i_partition]:
                    mask_view[jdx] = True

    return mask


def prune_filters_mask_csr(
    neighbors: np.ndarray,
    neighborhood_boundaries: np.ndarray,
    filters: List[np.ndarray],
    thresholds: Union[List, np.ndarray],
) -> np.ndarray:
    """Combines masks for multiple filters as produced by prune_filter_mask."""
    mask = np.ones(neighbors.shape, dtype=np.bool_)
    for f, thresh in zip(filters, thresholds):
        mask &= prune_filter_mask_csr(neighbors, neighborhood_boundaries, f, thresh)
    return mask


## Modularity computation


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def partition_modularity(
    neighbors: int32_t[::1],
    affinities: cython.float[:],
    neighborhood_boundaries: int32_t[::1],
    partition_vec: int32_t[::1],
) -> float:
    """Computes the modularity score of a given partition.

    It represents the difference between the (weighted) fraction of edges inside
    each set of the partition and the expected fraction of edges in that set if
    the graph were randomly rewired while preserving node degrees.

    It turns out that this can be calculated in a fairly straightforward way:
    for each partition set U, get the fraction of edges lying inside U, and
    subtract the squared fraction of edge ends inside U (or directed edges
    beginning in U), and sum these together.
    """

    in_community_weights = np.zeros(np.max(partition_vec) + 1, dtype=np.float32)
    total_community_weights = np.zeros_like(in_community_weights)
    in_community_weights_view = cython.declare(cython.float[::1], in_community_weights)
    total_community_weights_view = cython.declare(
        cython.float[::1], total_community_weights
    )

    total_weight: cython.float = np.sum(affinities)

    # if there are no edges, we say modularity is 0 because the expected number
    # of edges is always equal to the actual number of edges
    # TODO: is there a better, more reasonable value?
    if total_weight <= 0:
        return 0

    N: cython.Py_ssize_t = len(neighborhood_boundaries) - 1
    i: cython.Py_ssize_t
    partition_i: int32_t
    jdx: cython.Py_ssize_t
    for i in range(N):
        partition_i = partition_vec[i]
        for jdx in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            if partition_vec[j] == partition_i:
                in_community_weights_view[partition_i] += affinities[jdx]
            total_community_weights_view[partition_i] += affinities[jdx]
    # note that because both directions of edges are stored, the
    # total_community_weights effectively counts endpoints of edges in each
    # community, which is what's desired.
    modularity = np.sum(
        in_community_weights / total_weight
        - (total_community_weights / total_weight) ** 2
    )
    return modularity


## Connected components


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.ccall
def assign_neighbors_iterative_csr(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    mask: cython.char[:],
    edge_ranks: int32_t[:],
    max_rank: int32_t,
    cpts: int32_t[::1],
    start_vtx: int32_t,
    current_cpt: int32_t,
):
    cpts[start_vtx] = current_cpt
    # stack of nodes we have visited but have not necessarily seen all neighbors
    vx_stack: vector[int32_t] = vector[int32_t]()
    vx_stack.push_back(start_vtx)
    # stores the index of the next neighbor to visit for each node in the stack to avoid
    # iterating through them all every time we return to a node
    jdx: int32_t = neighborhood_boundaries[start_vtx]
    jdx_stack: vector[int32_t] = vector[int32_t]()
    jdx_stack.push_back(jdx)

    i: int32_t
    j: int32_t

    while not vx_stack.empty():
        i = vx_stack.back()
        start_jdx = jdx_stack.back()

        for jdx in range(start_jdx, neighborhood_boundaries[i + 1]):
            j = neighbors[jdx]
            if cpts[j] != -1:
                continue
            if mask[jdx] and edge_ranks[jdx] < max_rank:
                cpts[j] = current_cpt
                vx_stack.push_back(j)
                jdx_stack[jdx_stack.size() - 1] = jdx + 1
                jdx_stack.push_back(neighborhood_boundaries[j])
                break
        else:
            # if there are no remaining unvisited neighbors, move back up the queue
            vx_stack.pop_back()
            jdx_stack.pop_back()


@cython.boundscheck(False)
@cython.wraparound(False)
def connected_components_masked_csr(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    edge_ranks: int32_t[:],
    mask: cython.char[:],
    max_rank: cython.int,
) -> np.ndarray:
    """Computes connected components of a masked CSR-format neighborhood graph.

    Returns a length-N array of integers giving an id for the component each
    node lies in.

    Assumes that the underlying graph described by the `neighbors` and
    `neighborhood_boundaries` arrays is undirected, so an edge i~j is
    represented as both i->j and j->i. The mask should also be undirected.
    """
    N = len(neighborhood_boundaries) - 1
    cpts = np.full(N, -1, dtype=np.int32)
    cpts_view = cython.declare(int32_t[::1], cpts)
    current_cpt = 0
    for i in range(N):
        if cpts_view[i] == -1:
            assign_neighbors_iterative_csr(
                neighbors,
                neighborhood_boundaries,
                mask,
                edge_ranks,
                max_rank,
                cpts,
                i,
                current_cpt,
            )
            current_cpt += 1

    return cpts
