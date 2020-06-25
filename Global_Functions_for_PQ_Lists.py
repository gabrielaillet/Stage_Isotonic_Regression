
"""
Contains function

sort_pi_qew_list(pi_qew_list):
    Given a PQ-Tree represented as a list "pi_qew_list", re-order the nodes of "pi_qew_list" such that we get a
    standard representation of a PQ-tree. It is then possible to test equality between PQ-Trees using '=='

"""

from Diverse_Functions import reverse_end_of_list
from Diverse_Functions import sort_the_end_by_values


P_NODE = 'P_node'
Q_NODE = 'Q_node'


def sort_pi_qew_list(pi_qew_list):
    if type(pi_qew_list) == int:
        return pi_qew_list
    values = ['not_used']
    for i in range(1, len(pi_qew_list)):
        values.append(sort_pi_qew_list(pi_qew_list[i]))
    if pi_qew_list[0] == Q_NODE and values[1] > values[-1]:
        reverse_end_of_list(pi_qew_list)
        values[1] = values[-1]
    elif pi_qew_list[0] == P_NODE:
        sort_the_end_by_values(pi_qew_list, values)
    return values[1]


__author__ = 'pascal'
