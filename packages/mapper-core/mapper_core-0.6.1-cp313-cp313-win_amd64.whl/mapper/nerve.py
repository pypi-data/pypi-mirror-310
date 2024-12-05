# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3
# distutils: language = c++

from typing import List, Tuple

import cython
import numpy as np
from cython.cimports.libc.stdint import int32_t
from cython.cimports.libcpp.map import map as stdmap
from cython.cimports.libcpp.pair import pair
from cython.cimports.libcpp.set import set as stdset
from cython.cimports.libcpp.vector import vector

bool_like = cython.fused_type(cython.char, cython.integral)


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing.
def partition_set_sizes(partition: int32_t[::1]) -> np.ndarray:
    """Returns the size of each set in a partition."""
    sizes = np.zeros(np.max(partition) + 1, dtype=np.int32)
    sizes_view = cython.declare(int32_t[::1], sizes)
    for i in partition:
        sizes_view[i] += 1
    return sizes


# TODO: make calls to numpy constructors via the C API
@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing.
def partition_vec_to_cover(partition_vec: cython.integral[::1]) -> List[np.ndarray]:
    """Converts a length-N vector whose entries give the partition set for each
    point into a list of lists."""
    # we assume that partitions are indexed contiguously beginning from 0,
    # although nothing breaks if a partition index is missing, just empty
    # arrays in the output. negative-indexed partitions are ignored

    # using stable sort means that the indices will already be sorted in each partition
    sort_idx = cython.declare(
        cython.Py_ssize_t[::1], np.argsort(partition_vec, kind="stable")
    )

    n_elts: cython.Py_ssize_t = partition_vec.shape[0]
    n_sets: cython.Py_ssize_t = partition_vec[sort_idx[n_elts - 1]] + 1

    cover = np.empty(n_sets, dtype=object)

    # this at least avoids crashing in the case where partition_vec has negative entries
    current_partition: int32_t = min(0, partition_vec[sort_idx[0]])
    last_idx: cython.Py_ssize_t = 0
    i: cython.Py_ssize_t

    for i in range(n_elts):
        val = partition_vec[sort_idx[i]]
        if val != current_partition:
            # we found the end of the current partition, so add it to the list
            cover[current_partition] = np.array(sort_idx[last_idx:i], dtype=np.int32)
            # now add empty sets for any missing sequential values
            for p in range(current_partition + 1, val):
                cover[p] = np.empty(0, dtype=np.int32)
            current_partition = val
            last_idx = i
    cover[current_partition] = np.array(sort_idx[last_idx:], dtype=np.int32)

    return cover.tolist()


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing.
@cython.cdivision(True)
def weighted_partition_graph_edge_list_csr(
    neighbors: int32_t[::1],
    weights: cython.float[:],
    neighborhood_boundaries: int32_t[::1],
    edge_ranks: int32_t[:],
    mask: bool_like[:],
    max_rank: int32_t,
    partition_vec: np.ndarray,
    cover: List[np.ndarray],
    normalize_weights: bool = True,
) -> Tuple[np.ndarray, np.ndarray]:
    """Edge-based approach to producing a partition graph. Requires both the
    membership vector and the list of sets representation. Assumes the graph and
    mask are symmetric."""

    # this is an attempt to be more clever, requiring more effort for
    # correctness.  it works by using the neighbors array as indices into the
    # partition membership vector, replacing each neighbor graph node index with
    # the index of a partition set. then, it pulls out the rows of this array
    # corresponding with each set in the partition, deduplicates them, and
    # extracts the edge pairs.

    should_normalize_weights: cython.char = normalize_weights

    partition_neighbors = partition_vec[neighbors].astype(np.int32)
    partition_neighbors_view = cython.declare(int32_t[::1], partition_neighbors)

    edge_list: vector[pair[int32_t, int32_t]] = vector[pair[int32_t, int32_t]]()
    edge_weights: vector[cython.float] = vector[cython.float]()

    u_nbrs: stdmap[int32_t, cython.float] = stdmap[int32_t, cython.float]()

    n_cover_sets: cython.Py_ssize_t = len(cover)
    udx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    i: cython.Py_ssize_t
    vdx: int32_t
    udx: int32_t
    u_size: cython.float
    v_size: cython.float
    edge_weight: cython.float

    cover_sizes: vector[int32_t] = vector[int32_t]()

    if should_normalize_weights:
        for udx in range(n_cover_sets):
            cover_sizes.push_back(cover[udx].shape[0])

    for udx in range(n_cover_sets):
        u = cover[udx]
        u_view = cython.declare(int32_t[::1], u)
        u_nbrs.clear()

        # accumulate the weights for all neighboring partitions of u
        j = 0
        for i in u_view:
            for j in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
                if mask[j] and (edge_ranks[j] < max_rank):
                    u_nbr = partition_neighbors_view[j]
                    u_nbr_weight = weights[j]
                    if u_nbrs.count(u_nbr) == 0:
                        u_nbrs[u_nbr] = u_nbr_weight
                    else:
                        u_nbrs[u_nbr] += u_nbr_weight

        # convert these partitions into the edge list/weights
        for entry in u_nbrs:
            # this always fails if vdx = -1
            vdx = entry.first
            if vdx > udx:
                edge_weight = entry.second
                if should_normalize_weights:
                    u_size = cover_sizes[udx]
                    v_size = cover_sizes[vdx]
                    edge_weight = edge_weight / (u_size * v_size)
                edge_list.push_back(pair[int32_t, int32_t](udx, vdx))
                edge_weights.push_back(edge_weight)

    # reorganize into arrays
    edge_array = np.empty((edge_list.size(), 2), dtype=np.int32)
    weights_array = np.empty(edge_list.size(), dtype=np.float32)
    edge_array_view = cython.declare(int32_t[:, ::1], edge_array)
    weights_array_view = cython.declare(cython.float[::1], weights_array)

    for i in range(edge_list.size()):
        edge_array_view[i, 0] = edge_list[i].first
        edge_array_view[i, 1] = edge_list[i].second
        weights_array_view[i] = edge_weights[i]

    return edge_array, weights_array
    # return edge_list, edge_weights


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing.
def partition_graph_edge_list_csr(
    neighbors: int32_t[::1],
    neighborhood_boundaries: int32_t[::1],
    edge_ranks: int32_t[::1],
    mask: bool_like[::1],
    max_rank: int32_t,
    partition_vec: np.ndarray,
    cover: List[np.ndarray],
) -> List[Tuple[int, int]]:
    """Edge-based approach to producing a partition graph. Requires both the
    membership vector and the list of sets representation. Assumes the graph and
    mask are symmetric."""

    partition_neighbors = partition_vec[neighbors].astype(np.int32)
    partition_neighbors_view = cython.declare(int32_t[::1], partition_neighbors)

    edge_list: vector[pair[int32_t, int32_t]] = vector[pair[int32_t, int32_t]]()

    u_nbrs: stdset[int32_t] = stdset[int32_t]()

    n_cover_sets: cython.Py_ssize_t = len(cover)
    udx: cython.Py_ssize_t
    j: cython.Py_ssize_t
    i: cython.Py_ssize_t
    vdx: int32_t
    udx: int32_t

    for udx in range(n_cover_sets):
        u = cover[udx]
        u_view = cython.declare(int32_t[::1], u)
        u_nbrs.clear()

        # accumulate the weights for all neighboring partitions of u
        j = 0
        for i in u_view:
            for j in range(neighborhood_boundaries[i], neighborhood_boundaries[i + 1]):
                if mask[j] and (edge_ranks[j] < max_rank):
                    u_nbr = partition_neighbors_view[j]
                    u_nbrs.insert(u_nbr)

        # convert these partitions into the edge list/weights
        for vdx in u_nbrs:
            # this always fails if vdx = -1
            if vdx > udx:
                edge_list.push_back(pair[int32_t, int32_t](udx, vdx))

    return edge_list
