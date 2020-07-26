__author__ = 'pascal'

""" The famous Booth & Lueker algorithm. self-contained

Based on the paper
    K.S. Booth & G.S. Lueker
    Testing for the Consecutive Ones Property, Interval Graphs and Graph Planarity Using PQ_Tree Algorithm
    Journal of Computer & System Science 13, 335-379
    1976

A good description of this algorithm (with another implementation) can be found at
    http://gregable.com/2008/11/pq-tree-algorithm-and-consecutive-ones.html

Contains the functions :

booth_and_lueker(set_of_subsets, points, randomized)
    given a set "points" (= {0,.. n-1}, and a set of subsets of "points" "set_oo_subsets", and a boolean "randomized"
    returns a pi_qwe_list [tree, accepted_or_not[0], accepted_or_not[1], accepted_sets] made of:
        - if possible : a PQ-tree "tree" which represents all the permutations of "points"
        such that each element of "set_of_subsets" is an interval.
        If this is not possible, "tree" is None.
        - the number of 'accepted' subsets ("accepted_or_not[0]"), i.e. which are intervals
        - the number of 'refused' subsets ("accepted_or_not[1]"). if "tree" is not None, this number is 0
        - the pi_qwe_list of the ranks of accepted sets (in "set_of_subsets"): "accepted_sets"
    If "randomized" is True, the sets in "set_of_subsets" are considered in random order.

update_tree(tree, subset, nb_of_points, nb_accepted_subsets, nb_refused_subsets, subset_characteristic)
    Given a PQ-tree "tree" on the set X = {0, .., "nb_of_points" -1}. The construction of "tree" was made with
    "nb_accepted_subsets" subsets, and "nb_refused_subsets" have been considered but were not compatible with
    (the current) "tree".
    Given a subset "subset" of X, with 'characteristic' "subset_characteristic" (this argument can be freely used):
    if "subset" is compatible with "tree":
        updates "tree" and "accepted_or_not[0]" (the nb of accepted subsets),
        returns [accepted_or_not[0], accepted_or_not[1], subset_characteristic]
    if "subset" is not compatible with "tree":
        leave "tree" unchanged and update the number of refused subsets ("accepted_or_not[1]")
        returns [accepted_or_not[0], accepted_or_not[1], None]


+ some other functions used by "robinson recognition":

add_to_the_end(node, tree)
    Given two PQ-trees "node" and 'tree", change "tree" by adding "node" as its last son.

remove(node, tree)
    Given a PQ-tree "tree" and one of its sons "node", remove "node" from "tree"

change_orientation(tree)
    Can be used with any PQ-tree "tree", but is interested only if "tree" is a Q-node.
    Inverse the order of the sons of "tree"


+ some less generic functions

A node of a PQ-tree is a structure (implemented as a dictionary) whose fields are described just below:
The fields "PORQ", "LEAF_SET", "PERE", "GD_FRERE", "PTI_FRERE", "CADET" and "AINE" are always used
The fields "FEPOP" and "NB_UN" are used by the Booth-and-Lueker algorithm
Such a structure is not well printable.
To visualize a PQ-tree, use functions in module "Type_Conversions_for_PQ-Tree"
"""


PORQ = 'Pnode_or_Qnode'  # the possible values are:
P_NODE = 'P_node'
Q_NODE = 'Q_node'
LEAF = 'leaf'
UNKNOWN = 'unknown'

FEPOP = 'Full_Empty_Partial_Or_Pertinent'  # the possible values are:
FULL = 'full'
EMPTY = 'empty'
PARTIAL = 'partial'
PERTINENT = 'pertinent'

LEAF_SET = 'leaf_set'
PERE = 'father'
GD_FRERE = 'great_brother'
PTI_FRERE = 'little_brother'
CADET = 'youngest_son'
AINE = 'oldest_son'
NB_UN = 'number_of_one'

import random


def booth_and_lueker(set_of_subsets, points, randomized=False, tree=None):
    if tree is None:
        tree = universal_tree(points)
    accepted_or_not = [0, 0]
    accepted_sets = []
    the_nums = list(range(len(set_of_subsets)))
    if randomized:
        random.shuffle(the_nums)
    for num_set in the_nums:
        subset = set_of_subsets[num_set]
        accepted_or_not = update_tree(tree, subset, len(points), accepted_or_not[0], accepted_or_not[1], num_set)
        if accepted_or_not[2] is not None:
            accepted_sets.append(accepted_or_not[2])
    return [tree, accepted_or_not[0], accepted_or_not[1], accepted_sets]


def update_tree(tree, subset, nb_of_points, nb_accepted_subsets, nb_refused_subsets, subset_characteristic):
    if 1 < len(subset) < nb_of_points:
        the_line = [0] * nb_of_points
        for i in subset:
            the_line[i] = 1
        counting_the_ones(tree, the_line)
        pertinent_node = detection_pertinent(tree, len(subset))
        update_fepop(pertinent_node)
        if pertinent_node[FEPOP] != FULL:
            pertinent_node[FEPOP] = PERTINENT
            if not good_node(pertinent_node, True):
                return [nb_accepted_subsets, nb_refused_subsets + 1, None]
            reduction(pertinent_node)
    return [nb_accepted_subsets + 1, nb_refused_subsets, subset_characteristic]


def build_node(t_ype, fep, leaf_set, father, great_brother, little_brother, small_son, big_son, number_of_one):
    return {PORQ: t_ype,
            FEPOP: fep,
            LEAF_SET: leaf_set,
            PERE: father,
            GD_FRERE: great_brother,
            PTI_FRERE: little_brother,
            CADET: small_son,
            AINE: big_son,
            NB_UN: number_of_one}


def universal_tree(points):
    root = build_node(P_NODE, UNKNOWN, points, None, None, None, None, None, 0)
    if len(points) > 0:
        root[CADET] = build_node(LEAF, UNKNOWN, [points[0]], root, None, None, None, None, 0)
        current_son = root[CADET]
        for pt in points[1:]:
            current_son[GD_FRERE] = build_node(LEAF, UNKNOWN, [pt], root, None, current_son, None, None, 1)
            current_son = current_son[GD_FRERE]
        root[AINE] = current_son
        return root


def update_fepop(node):
    if node[PORQ] == LEAF:
        if node[NB_UN] == 1:
            node[FEPOP] = FULL
        else:
            node[FEPOP] = EMPTY
    else:
        current_son = node[CADET]
        while current_son is not None:
            update_fepop(current_son)
            current_son = current_son[GD_FRERE]
        full_empty_partial = counting_fep(node)
        if full_empty_partial[2] != 0:
            node[FEPOP] = PARTIAL
        elif full_empty_partial[1] == 0:
            node[FEPOP] = FULL
        elif full_empty_partial[0] == 0:
            node[FEPOP] = EMPTY
        else:
            node[FEPOP] = PARTIAL


def counting_fep(node):
    full_empty_partial = [0, 0, 0]
    current_son = node[CADET]
    while current_son is not None:
        if current_son[FEPOP] == FULL:
            full_empty_partial[0] += 1
        elif current_son[FEPOP] == EMPTY:
            full_empty_partial[1] += 1
        elif current_son[FEPOP] == PARTIAL:
            full_empty_partial[2] += 1
        current_son = current_son[GD_FRERE]
    return full_empty_partial


def counting_the_ones(node, line):
    if node[PORQ] == LEAF:
        node[NB_UN] = line[node[LEAF_SET][0]]
        return node[NB_UN]
    current_son = node[CADET]
    nb_of_ones = 0
    while current_son is not None:
        nb_of_ones += counting_the_ones(current_son, line)
        current_son = current_son[GD_FRERE]
    node[NB_UN] = nb_of_ones
    return nb_of_ones


def detection_pertinent(node, length):
    if node[NB_UN] == length:
        current_son = node[CADET]
        while (current_son is not None) and (current_son[NB_UN] != length):
            current_son = current_son[GD_FRERE]
        if current_son is None:
            return node
        return detection_pertinent(current_son, length)


def reduction(node):
    if node[FEPOP] == PARTIAL or node[FEPOP] == PERTINENT:
        current_son = node[CADET]
        while current_son is not None:
            reduction(current_son)
            current_son = current_son[GD_FRERE]
        treatment(node)


def good_node(tree, boolean):
    if not boolean:
        return False
    if tree[FEPOP] == PARTIAL or tree[FEPOP] == PERTINENT:
        current_son = tree[CADET]
        while current_son is not None:
            boolean = good_node(current_son, boolean)
            current_son = current_son[GD_FRERE]
        return verification_node(tree, boolean)
    return True


def verification_node(tree, boolean):
    nb_partial = counting_fep(tree)[2]
    if not boolean or nb_partial > 2 or (tree[FEPOP] != PERTINENT and nb_partial == 2):
        return False
    if tree[PORQ] == Q_NODE:
        boolean = verification_consecutive(tree)
        if tree[FEPOP] == PARTIAL:
            boolean = boolean and not_in_middle(tree)
    return boolean


def not_in_middle(tree):
    if tree[CADET][FEPOP] == FULL or tree[AINE][FEPOP] == FULL:
        return True
    if tree[CADET][FEPOP] == PARTIAL and tree[CADET][GD_FRERE][FEPOP] == EMPTY:
        return True
    if tree[AINE][FEPOP] == PARTIAL and tree[AINE][PTI_FRERE][FEPOP] == EMPTY:
        return True
    return False


def verification_consecutive(tree):
    state = "begin"
    current_node = tree[CADET]
    while current_node is not None:
        if current_node[FEPOP] == EMPTY:
            if state in ["second_partial", "full", "first_partial"]:
                state = "end"
        elif current_node[FEPOP] == FULL:
            if state in ["second_partial", "end"]:
                return False
            state = "full"
        elif current_node[FEPOP] == PARTIAL:
            if state in ["second_partial", "end"]:
                return False
            if state in ["first_partial", "full"]:
                state = "second_partial"
            elif state == "begin":
                state = "first_partial"
        current_node = current_node[GD_FRERE]
    return True


def treatment(node):
    pattern = case_determination(node)
    case_treatment(pattern, node)


def case_determination(node):
    nb_of_partial = counting_fep(node)[2]
    if nb_of_partial <= 2:
        return [node[PORQ], node[FEPOP], nb_of_partial]


def case_treatment(pattern, node):
    if pattern == [P_NODE, PERTINENT, 0]:
        do_pattern_pi_2(node)
    elif pattern == [P_NODE, PARTIAL, 0]:
        do_pattern_pi_3(node)
    elif pattern == [P_NODE, PERTINENT, 1]:
        do_pattern_pi_4(node)
    elif pattern == [P_NODE, PARTIAL, 1]:
        do_pattern_pi_5(node)
    elif pattern == [P_NODE, PERTINENT, 2]:
        do_pattern_pi_6(node)
    elif pattern[0] == Q_NODE and pattern[2] == 1:
        do_pattern_qew_2(node)
    elif pattern == [Q_NODE, PERTINENT, 2]:
        do_pattern_qew_3(node)


def do_pattern_qew_3(tree):
    first_partial_son = search_sons_fepop_rank(tree, PARTIAL, 1)
    second_partial_son = search_sons_fepop_rank(tree, PARTIAL, 2)
    orient_fepop_first(first_partial_son, EMPTY)
    orient_fepop_first(second_partial_son, FULL)
    put_sons_of_into(first_partial_son, tree)
    put_sons_of_into(second_partial_son, tree)


def do_pattern_qew_2(tree):
    partial_son = search_sons_fepop_rank(tree, PARTIAL, 1)
    if bad_oriented(partial_son):
        change_orientation(partial_son)
    put_sons_of_into(partial_son, tree)


def put_sons_of_into(node, tree):
    if node[PTI_FRERE] is None:
        tree[CADET] = node[CADET]
        tree[CADET][PERE] = tree
    else:
        node[CADET][PTI_FRERE] = node[PTI_FRERE]
        node[PTI_FRERE][GD_FRERE] = node[CADET]
        node[CADET][PERE] = tree
    if node[GD_FRERE] is None:
        tree[AINE] = node[AINE]
        tree[AINE][PERE] = tree
    else:
        node[AINE][GD_FRERE] = node[GD_FRERE]
        node[GD_FRERE][PTI_FRERE] = node[AINE]
        node[AINE][PERE] = tree
    destroy(node)


def bad_oriented(node):
    result_1 = node[PTI_FRERE] is not None and node[PTI_FRERE][FEPOP] != node[CADET][FEPOP]
    result_2 = node[GD_FRERE] is not None and node[GD_FRERE][FEPOP] != node[AINE][FEPOP]
    return result_1 or result_2


def do_pattern_pi_6(tree):
    first_partial_son = search_sons_fepop_rank(tree, PARTIAL, 1)
    second_partial_son = search_sons_fepop_rank(tree, PARTIAL, 2)
    full_son = put_sons_together(tree, FULL)
    orient_fepop_first(first_partial_son, EMPTY)
    add_to_the_end(full_son, first_partial_son)
    orient_fepop_first(second_partial_son, FULL)
    partial_son = fusion_qew_nodes(first_partial_son, second_partial_son, tree)
    if counting_fep(tree)[1] == 0:
        replace_father_by_unique_son(tree, partial_son)


def fusion_qew_nodes(first_node, second_node, tree):
    first_node[AINE][GD_FRERE] = second_node[CADET]
    second_node[CADET][PTI_FRERE] = first_node[AINE]
    first_node[AINE][PERE] = None
    second_node[CADET][PERE] = None
    first_node[AINE] = second_node[AINE]
    first_node[AINE][PERE] = first_node
    remove(second_node, tree)
    destroy(second_node)
    return first_node


def orient_fepop_first(tree, type_fepop):
    if tree[CADET][FEPOP] != type_fepop and tree[AINE][FEPOP] == type_fepop:
        change_orientation(tree)


def change_orientation(tree):
    node = tree[CADET]
    while node is not None:
        node[GD_FRERE], node[PTI_FRERE] = node[PTI_FRERE], node[GD_FRERE]
        node = node[PTI_FRERE]
    tree[CADET], tree[AINE] = tree[AINE], tree[CADET]


def do_pattern_pi_5(tree):
    partial_son = search_sons_fepop_rank(tree, PARTIAL, 1)
    full_son = put_sons_together(tree, FULL)
    empty_son = put_sons_together(tree, EMPTY)
    if partial_son[AINE][FEPOP] == FULL:
        add_to_the_end(full_son, partial_son)
        add_to_the_beginning(empty_son, partial_son)
    else:
        add_to_the_end(empty_son, partial_son)
        add_to_the_beginning(full_son, partial_son)
    replace_father_by_unique_son(tree, partial_son)


def do_pattern_pi_4(tree):
    partial_son = search_sons_fepop_rank(tree, PARTIAL, 1)
    full_empty_partial = counting_fep(tree)
    if full_empty_partial[1] == 0:
        do_pattern_pi_5(tree)
    else:
        if full_empty_partial[0] == 1:
            full_son = search_sons_fepop_rank(tree, FULL, 1)
        else:
            put_sons_together_to_the_end(tree, FULL)
            full_son = tree[AINE]
        remove(full_son, tree)
        if partial_son[AINE][FEPOP] == FULL:
            add_to_the_end(full_son, partial_son)
            full_son[PTI_FRERE][PERE] = None
        elif partial_son[CADET][FEPOP] == FULL:
            add_to_the_beginning(full_son, partial_son)
            full_son[GD_FRERE][PERE] = None


def do_pattern_pi_3(node):
    full_empty_partial = counting_fep(node)
    nb_full = full_empty_partial[0]
    nb_empty = full_empty_partial[1]
    if nb_full > 1:
        put_sons_together_to_the_end(node, FULL)
    if nb_empty > 1:
        put_sons_together_to_the_end(node, EMPTY)
    node[PORQ] = Q_NODE


def do_pattern_pi_2(node):
    full_empty_partial = counting_fep(node)
    if full_empty_partial[0] > 1 and full_empty_partial[1] > 0:
        put_sons_together_to_the_end(node, FULL)


def put_sons_together_to_the_end(tree, type_fepop):
    node = put_sons_together(tree, type_fepop)
    add_to_the_end(node, tree)


def add_to_the_end(node, tree):
    if node is not None:
        if tree[CADET] is None:
            tree[CADET] = node
        else:
            tree[AINE][GD_FRERE] = node
            if (tree[AINE][PTI_FRERE] is not None) and (tree[PORQ] == Q_NODE):
                tree[AINE][PERE] = None
        node[PTI_FRERE] = tree[AINE]
        tree[AINE] = node
        node[PERE] = tree
        node[GD_FRERE] = None
        if NB_UN in node:
            tree[NB_UN] += node[NB_UN]


def add_to_the_beginning(node, tree):
    if node is not None:
        if tree[AINE] is None:
            tree[AINE] = node
        else:
            tree[CADET][PTI_FRERE] = node
            if tree[CADET][GD_FRERE] is not None and tree[PORQ] == Q_NODE:
                tree[CADET][PERE] = None
        node[GD_FRERE] = tree[CADET]
        tree[CADET] = node
        node[PERE] = tree
        node[PTI_FRERE] = None
        if NB_UN in node:
            tree[NB_UN] += node[NB_UN]


def remove(node, tree):
    if node is not None:
        if node[PTI_FRERE] is None:
            tree[CADET] = node[GD_FRERE]
            if node[GD_FRERE] is not None:
                node[GD_FRERE][PERE] = tree
        else:
            node[PTI_FRERE][GD_FRERE] = node[GD_FRERE]
        if node[GD_FRERE] is None:
            tree[AINE] = node[PTI_FRERE]
            if node[PTI_FRERE] is not None:
                node[PTI_FRERE][PERE] = tree
        else:
            node[GD_FRERE][PTI_FRERE] = node[PTI_FRERE]
        if NB_UN in node:
            tree[NB_UN] -= node[NB_UN]


def replace_father_by_unique_son(tree, node):
    tree[CADET] = node[CADET]
    tree[AINE] = node[AINE]
    tree[FEPOP] = node[FEPOP]
    tree[PORQ] = node[PORQ]
    node[CADET][PERE] = tree
    node[AINE][PERE] = tree
    destroy(node)


def destroy(tree):
    tree[GD_FRERE], tree[PTI_FRERE], tree[PERE], tree[CADET], tree[AINE] = None, None, None, None, None
    del tree


def put_sons_together(tree, type_fepop):
    full_empty_partial = counting_fep(tree)
    index = [FULL, EMPTY, PARTIAL].index(type_fepop)
    node = None
    if full_empty_partial[index] == 1:
        node = search_sons_fepop_rank(tree, type_fepop, 1)
        remove(node, tree)
    elif full_empty_partial[index] > 1:
        current_son = tree[CADET]
        node = build_node(P_NODE, type_fepop, [], None, None, None, None, None, 0)
        while current_son is not None:
            follower = current_son[GD_FRERE]
            if current_son[FEPOP] == type_fepop:
                remove(current_son, tree)
                add_to_the_end(current_son, node)
                node[NB_UN] += current_son[NB_UN]
            current_son = follower
    return node


def search_sons_fepop_rank(tree, type_fepop, rank):
    result = None
    node = tree[CADET]
    k = 0
    while (node is not None) and (k < rank):
        if node[FEPOP] == type_fepop:
            k += 1
            result = node
        node = node[GD_FRERE]
    if k == rank:
        return result