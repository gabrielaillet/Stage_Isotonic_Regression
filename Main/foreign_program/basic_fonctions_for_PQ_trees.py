__author__ = 'pascal'


"""Contains the functions:

characteristic_subset_set_of(tree)
    an inverse of the Booth-and-Lueker algorithm :
    returns ALL the subsets (of the underlying set) which are intervals for all the permutation represented by
    the PQ-tree "tree"

characteristic_subset_list_of(tree):
    used by characteristic_subset_set_of(tree).
    gives the result as a pi_qwe_list. characteristic_subset_set_of(tree) gives it as a set.
    USES THE FUNCTIONS "put_off_singletons" and "list_fusion" FROM THE LIBRARY "Diverse_Functions"

minimal_subset_set_of(tree)
    an inverse of the Booth-and-Lueker algorithm :
    returns a MINIMAL set S of subsets (of the underlying set) which are intervals for all the permutation
    represented by the PQ-tree "tree". It is possible, from S, to retrieve the PQ-tree "tree"
    USES THE FUNCTIONS "put_off_singletons" and "list_fusion" FROM THE LIBRARY "Diverse_Functions"

number_of_permutations_represented_by(PQ-tree)

robinson_verification(tree, distance):
    verify if a (one) permutation represented by the PQ-tree "tree" is a compatible order for "distance"

number_of_sons(tree)
    returns the number of sons at the root of the tree "tree"

depth(tree)

ordered_course(tree, vector)
    Given a PQ-Tree "tree", add the ordered pi_qwe_list of its leaves at the end of "vector"
    Should be used with "vector" = []. In this case, at the end, "vector" is one of the permutations
    represented by "tree".

update_father_and_leaf_sets(tree)


+ other less generic functions, generally used by the library "robinson_recognition.py"


A node of a PQ-tree is a structure (implemented as a dictionary) whose fields are described just below:
The fields "PORQ", "LEAF_SET", "PERE", "GD_FRERE", "PTI_FRERE", "CADET" and "AINE" are always used
The fields "FEPOP" and "NB_UN" are used by the Booth-and-Lueker algorithm
The field "REPRESENTATIVE" is used by robinson recognition.
Such a structure is not well printable.
To visualize a PQ-tree, use functions in module "Type_Conversions_for_PQ-Tree"
"""


PORQ = 'Pnode_or_Qnode'  # the possible values are:
P_NODE = 'P_node'
Q_NODE = 'Q_node'
LEAF = 'leaf'
UNKNOWN = 'unknown'

LEAF_SET = 'leaf_set'
PERE = 'father'
GD_FRERE = 'great_brother'
PTI_FRERE = 'little_brother'
CADET = 'youngest_son'
AINE = 'oldest_son'

FEPOP = 'Full_Empty_Partial_Or_Pertinent'  # the possible values are:
FULL = 'full'
EMPTY = 'empty'
PARTIAL = 'partial'
PERTINENT = 'pertinent'

NB_UN = 'number_of_one'

REPRESENTATIVE = 'representative'


from Main.foreign_program.Diverse_Functions import put_off_singletons
from Main.foreign_program.Diverse_Functions import list_fusion

import math


#####################################################################################

def characteristic_subset_set_of(tree):
    update_father_and_leaf_sets(tree)
    the_list = characteristic_subset_list_of(tree)
    result = set()
    for subset in the_list:
        result.add(subset)
    return result


def characteristic_subset_list_of(tree):
    the_subsets = []
    if tree is not None:
        tree[LEAF_SET].sort()
        the_subsets = [tuple(tree[LEAF_SET])]
        if tree[PORQ] != LEAF:
            node = tree[CADET]
            while node is not None:
                the_subsets.extend(characteristic_subset_list_of(node))
                node = node[GD_FRERE]
        if tree[PORQ] == Q_NODE and tree[CADET][GD_FRERE] is not None and tree[CADET][GD_FRERE][GD_FRERE]is not None:
            node = tree[CADET]
            while node[GD_FRERE] is not None:
                current_subset = node[LEAF_SET]
                current_node = node[GD_FRERE]
                while current_node is not None:
                    current_subset = list_fusion(current_subset, current_node[LEAF_SET])
                    the_subsets.append(tuple(current_subset))
                    current_node = current_node[GD_FRERE]
                node = node[GD_FRERE]
        if tree[PORQ] != LEAF:
            the_subsets = put_off_singletons(the_subsets)
    return the_subsets

####################################################################################


def minimal_subset_set_of(tree):
    update_father_and_leaf_sets(tree)
    the_subsets = set()
    if tree is not None:
        tree[LEAF_SET].sort()
        the_subsets = {tuple(tree[LEAF_SET])}
        if tree[PORQ] != LEAF:
            node = tree[CADET]
            while node is not None:
                the_subsets = the_subsets.union(minimal_subset_set_of(node))
                node = node[GD_FRERE]
        if tree[PORQ] == Q_NODE and tree[CADET][GD_FRERE] is not None and tree[CADET][GD_FRERE][GD_FRERE] is not None:
            node = tree[CADET]
            following_node = node[GD_FRERE]
            while following_node is not None:
                the_subsets.add(tuple(list_fusion(node[LEAF_SET], following_node[LEAF_SET])))
                node = node[GD_FRERE]
                following_node = following_node[GD_FRERE]
        if tree[PORQ] != LEAF:
            the_subsets = put_off_singletons(the_subsets)
    return the_subsets


def number_of_permutations_represented_by(tree):
    if tree is not None:
        number = 1
        if tree[PORQ] == Q_NODE:
            number = 2
        elif tree[PORQ] == P_NODE:
            number = math.factorial(number_of_sons(tree))
        node = tree[CADET]
        while node is not None:
            number *= number_of_permutations_represented_by(node)
            node = node[GD_FRERE]
        return number
    return 0


##################################################################################

def robinson_verification(tree, distance):
    vector = []
    ordered_course(tree, vector)
    return vector_verification(vector, distance)


def vector_verification(vector, distance):
    good = True
    for i in range(len(vector)):
        for j in range(i):
            if distance[vector[i]][vector[j]] < distance[vector[i]][vector[j + 1]]:
                good = False
        for j in range(i, len(vector) - 1):
            if distance[vector[i]][vector[j]] > distance[vector[i]][vector[j + 1]]:
                good = False
    return good

####################################################################################


def number_of_sons(tree):
    number = 0
    node = tree[CADET]
    while node is not None:
        number += 1
        node = node[GD_FRERE]
    return number


def depth(tree):
    if tree is None or tree[PORQ] == LEAF:
        return 0
    node = tree[CADET]
    value = 0
    while node is not None:
        local_value = depth(node)
        if local_value > value:
            value = local_value
        node = node[GD_FRERE]
    return 1 + value


def two_ball_from_three(reference_pt, pt_a, pt_b, distance, ancestor):
    close_pt = pt_a
    if distance[reference_pt][pt_b] < distance[reference_pt][pt_a]:
        close_pt = pt_b
    ref_dist = distance[reference_pt][close_pt]
    the_two_ball = []
    for x in ancestor[LEAF_SET]:
        if distance[x][reference_pt] <= ref_dist and distance[x][close_pt] <= ref_dist:
            the_two_ball.append(x)
    return the_two_ball


def ordered_course(tree, vector):
    if tree[PORQ] == LEAF:
        vector.append(tree[LEAF_SET][0])
    else:
        current_node = tree[CADET]
        while current_node is not None:
            ordered_course(current_node, vector)
            current_node = current_node[GD_FRERE]


def update_father_and_leaf_sets(tree):
    if tree is not None:
        if tree[PORQ] != LEAF:
            tree[LEAF_SET] = []

            current_node = tree[CADET]
            while current_node is not None:
                current_node[PERE] = tree
                update_father_and_leaf_sets(current_node)
                tree[LEAF_SET] += current_node[LEAF_SET]
                current_node = current_node[GD_FRERE]


def suppression_of_unique_sons(tree):
    did_something = False
    if tree[PORQ] != LEAF:
        current_node = tree[CADET]
        while current_node is not None:
            did_something = suppression_of_unique_sons(current_node) or did_something
            current_node = current_node[GD_FRERE]
        if tree[CADET][GD_FRERE] is None:
            tree[PORQ] = tree[CADET][PORQ]
            tree[AINE] = tree[CADET][AINE]
            tree[CADET] = tree[CADET][CADET]
            did_something = True
    return did_something


def representative_construction(tree):
    if tree[PORQ] != LEAF:
        current_node = tree[CADET]
        while current_node is not None:
            representative_construction(current_node)
            current_node = current_node[GD_FRERE]
    if tree[PORQ] != Q_NODE:
        tree[REPRESENTATIVE] = [tree[LEAF_SET][0], tree[LEAF_SET][0]]
    else:
        tree[REPRESENTATIVE] = [tree[CADET][REPRESENTATIVE][0], tree[AINE][REPRESENTATIVE][0]]