# Copyright (C) 2022-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

# cython: infer_types=True, language_level=3, annotation_typing=False
# distutils: language = c++
"""Interface to Mapper."""

from typing import Dict, Literal, Optional

import numpy as np

from mapper.multiresolution import HierarchicalPartitionGraph
from mapper.neighborgraph import NeighborGraph


def quick_graph(
    X: np.ndarray,
    metric: str,
    neighbor_params: Optional[Dict] = None,
    affinity: Literal["slpi", "exponential", "gaussian"] = "slpi",
):
    """Create a graph from a dataset and specified metric.

    If neighbor_params is not specified, chooses neighborhood parameters
    automatically. If it is specified, it must be a dictionary containing keys
    "M", "K", and "min_nbrs" with integer values. Increasing any of these values
    will increase the connectivity of the resulting graph."""

    if neighbor_params is None:
        ng = NeighborGraph.with_automatic_params(X, metric)
    else:
        neighbor_params["metric"] = metric
        ng = NeighborGraph(X, **neighbor_params)
    g = HierarchicalPartitionGraph(ng, affinity=affinity)
    return g
