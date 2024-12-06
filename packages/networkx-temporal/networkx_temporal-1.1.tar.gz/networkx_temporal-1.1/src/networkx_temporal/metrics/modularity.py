from functools import reduce
from operator import or_
from typing import Any, Optional, Union

from ..typing import TemporalGraph, StaticGraph


def modularity(
    TG: Union[TemporalGraph, StaticGraph],
    membership: Union[dict, list],
    weight: Union[bool, str] = True,
) -> Union[dict, int]:
    """
    Returns modularity of temporal graph snapshots.

    :param TG: A temporal graph.
    :param membership: A dictionary or a list of dictionaries where keys are nodes and values are
        static or dynamic community labels, respectively. If a list of dictionaries is provided, the
        length of the list must be equal to the number of snapshots in the temporal graph.
    :param weight: If True, use edge weights to compute modularity.
    """
    if isinstance(membership, dict):
        membership = [membership] * len(TG.snapshots)

    if len(membership) != len(TG.snapshots):
        raise ValueError("The length of 'membership' must be equal to the number of snapshots in the temporal graph.")

    return [
        _modularity(TG[t], membership[t] if type(membership) == list else membership, weight=weight)
        for t in range(len(TG))
    ]


def _modularity(G: StaticGraph, membership: dict, weight: Union[bool, str] = True) -> float:
    """
    Returns modularity of a graph.

    :param G: A graph.
    :param membership: A dictionary where keys are nodes and values are community labels.
    """
    if weight is True:
        weight = "weight"
    # if weight is False:
    #     weight = None

    q = 0
    m = G.size(weight=weight)

    for u, v, w in G.edges(data=weight, default=1):
        if membership[u] == membership[v]:
            q += w - G.degree(u) * G.degree(v) / (2 * m)

    return q / (2 * m)


# def snapshot_modularity(
#     snapshot: Any,
#     membership: dict,
# ) -> int:
#     """
#     Returns modularity of a temporal graph snapshot.

#     :param snapshot: A snapshot of a temporal graph.
#     :param membership: A dictionary where keys are nodes and values are static or dynamic community labels.
#     """
#     if not isinstance(membership, dict):
#         raise ValueError("The 'membership' parameter must be a dictionary.")

#     if not membership:
#         raise ValueError("The 'membership' dictionary must not be empty.")

#     if not all(isinstance(label, int) for label in membership.values()):
#         raise ValueError("The values of the 'membership' dictionary must be integers.")

#     # Get total number of communities.
#     communities = set(membership.values())

#     # Get total number of edges.
#     num_edges = snapshot.number_of_edges()

#     # Get total sum of node degree.
#     degrees = snapshot.degree()

#     # Get the sum of the degrees of the nodes in each community
#     sum_degrees_community = {community: 0 for community in communities}
#     for node, degree in degrees.items():
#         community = membership[node]
#         sum_degrees_community[community] += degree

#     # Get the sum of the degrees of the nodes in each community
#     sum_edges_community = {community: 0 for community in communities}
#     for edge in snapshot.edges():
#         node1, node2 = edge
#         community1 = membership[node1]
#         community2 = membership[node2]
#         if community1 == community2:
#             sum_edges_community[community1] += 1

#     # Calculate the modularity
#     modularity = 0
#     for community in communities:
#         modularity += sum_edges_community[community] / num_edges - (sum_degrees_community[community] / (2 * num_edges)) ** 2

#     return modularity