
"""
Contains the functions:

from_pi_qew_tree_to_string(tree, string=''):
    transforms a PQ_tree in a suitable string (for printing). usually to be used with "string" = '' (by default).
    More precisely, given a PQ-tree "tree" and a string "string", returns a string made of the concatenation of
    "string" and a representation of "tree",
            e.g. '{P_{Q_[9][3][1]}{P_[0][6][7]{P_[8][5]{P_[4][2]}}}}'


from_pi_qew_string_to_list(pi_qew_tree_as_a_string):
    This function was written in 2015 by Soufiane MALLEM during his L3-MPCI internship.

    Given a string "pi_qew_tree_as_a_string" (which represents a PQ-tree)
            e.g. '{P_{Q_[9][3][1]}{P_[0][6][7]{P_[8][5]{P_[4][2]}}}}'
    Returns a list representation of this PQ-tree,
            e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]


from_pi_qew_list_to_graphics(pi_qew_tree_as_a_list):
    This function was written in 2015 by Soufiane MALLEM during his L3-MPCI internship.

    Given a list or a tuple "pi_qew_tree_as_a_list" (which represents a PQ-tree),
            e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]
              or ('P_node', ('Q_node', 9, 3, 1), ('P_node', 0, 6, 7, ('P_node', 8, 5, ('P_node', 4, 2))))
    Draw this PQ-tree
    USES THE STANDARD MODULES matplotlib, random AND os.
    USES LIBRARY graphical_functions


from_pi_qew_list_to_tree(pi_qew_tree_as_a_list):
    Given a list or a tuple "pi_qew_tree_as_a_list" (which represents a PQ-tree),
            e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]
              or ('P_node', ('Q_node', 9, 3, 1), ('P_node', 0, 6, 7, ('P_node', 8, 5, ('P_node', 4, 2))))
    Returns this PQ-tree, as described below.
    USES FUNCTION "update_father_and_leaf_sets" FROM LIBRARY "basic_functions_for_PQ_trees"


from_pi_qew_tree_to_list(tree):
    Given a PQ-tree "tree", returns a list which represents it,
            e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]


from_pi_qew_list_to_string(pi_qew_list, string=''):
    Given a list or a tuple "pi_qew_tree_as_a_list" (which represents a PQ-tree),
            e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]
              or ('P_node', ('Q_node', 9, 3, 1), ('P_node', 0, 6, 7, ('P_node', 8, 5, ('P_node', 4, 2))))
    and a string "string".
    Returns a string made of the concatenation of "string" and a representation of the PQ-tree,
            e.g. '{P_{Q_[9][3][1]}{P_[0][6][7]{P_[8][5]{P_[4][2]}}}}'
    usually to be used with "string" = '' (by default).


from_pi_qew_list_to_tuple(pi_qew_list):
    Given a list "pi_qew_list" (which represents a PQ-tree)
            e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]
    returns a tuple that represent the same PQ-Tree,
            e.g. ('P_node', ('Q_node', 9, 3, 1), ('P_node', 0, 6, 7, ('P_node', 8, 5, ('P_node', 4, 2))))



A node of a PQ-tree is a structure (implemented as a dictionary) whose main fields are described just below.
Such a structure is not well printable.
To visualize a PQ-tree, use functions in this module.
"""


from Program.basic_fonctions_for_PQ_trees import update_father_and_leaf_sets


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


def from_pi_qew_tree_to_string(tree, string=''):
    if tree is None:
        return string + 'tree = None'
    if tree[PORQ] == LEAF:
        return string + str(tree[LEAF_SET])
    else:
        string = string + '{' + tree[PORQ][: 2]
        current_node = tree[CADET]
        while current_node is not None:
            string = from_pi_qew_tree_to_string(current_node, string)
            current_node = current_node[GD_FRERE]
        return string + '}'


##############################################################################################################

def from_pi_qew_string_to_list(pi_qew_tree_as_a_string):
    return list_filling(list(pi_qew_tree_as_a_string[1:]), [])[0]


def list_filling(pi_qew_string, tree_as_a_list):
    decimal_list = decimal_item()
    i = 0
    while i < len(pi_qew_string):
        if pi_qew_string[i] == 'Q':
            tree_as_a_list.append(Q_NODE)
            i += 1
        elif pi_qew_string[i] == 'P':
            tree_as_a_list.append(P_NODE)
            i += 1
        elif pi_qew_string[i] in decimal_list:
            leaf = pi_qew_string[i]
            j = i + 1
            while j < len(pi_qew_string) and pi_qew_string[j] != ']':
                leaf = leaf + pi_qew_string[j]
                j += 1
            tree_as_a_list.append(int(leaf))
            i = j
        elif pi_qew_string[i] == '{':
            (a, b) = (list_filling(pi_qew_string[i + 1:], [])[0], i + list_filling(pi_qew_string[i + 1:], [])[1] + 1)
            tree_as_a_list.append(a)
            i = b
        elif pi_qew_string[i] == '}':
            i += 1
            return [tree_as_a_list, i]
        else:
            i += 1


def decimal_item():
    list_of_digits = []
    for i in range(10):
        list_of_digits.append(str(i))
    return list_of_digits

################################################################################################################


def from_pi_qew_list_to_graphics(pi_qew_tree_as_a_list):
#    from seriation.graphical_functions import from_pi_qew_list_to_graphics_real
#    from_pi_qew_list_to_graphics_real(pi_qew_tree_as_a_list)
    pass

################################################################################################################


def from_pi_qew_list_to_tree(pi_qew_tree_as_a_list):
    tree = tree_completion(pi_qew_tree_as_a_list)
    update_father_and_leaf_sets(tree)
    return tree


def tree_completion(the_list):
    tree = {PORQ: the_list[0], PERE: None, PTI_FRERE: None, GD_FRERE: None}
    previous_node, node = None, None
    for element in the_list[1:]:
        if type(element) == int:
            node = {PORQ: LEAF, LEAF_SET: [element], PTI_FRERE: previous_node, PERE: tree, GD_FRERE: None}
        else:
            node = tree_completion(element)
            node[PTI_FRERE] = previous_node
            node[PERE] = tree
        if previous_node is None:
            tree[CADET] = node
        else:
            previous_node[GD_FRERE] = node
        previous_node = node
    tree[AINE] = node
    return tree

################################################################################################################


def from_pi_qew_tree_to_list(tree):
    if tree is not None and tree[PORQ] != LEAF:
        the_list = [tree[PORQ]]
        node = tree[CADET]
        while node is not None:
            if node[PORQ] == LEAF:
                the_list.append(node[LEAF_SET][0])
            else:
                the_list.append(from_pi_qew_tree_to_list(node))
            node = node[GD_FRERE]
        return the_list


def from_pi_qew_list_to_string(pi_qew_list, string=''):
    if len(pi_qew_list) == 0:
        return string + ' liste vide'
    string += '{' + pi_qew_list[0][: 2]
    for i in range(len(pi_qew_list))[1:]:
        if type(pi_qew_list[i]) == int:
            string = string + '[' + str(pi_qew_list[i]) + ']'
        else:
            string += from_pi_qew_list_to_string(pi_qew_list[i], '')
    return string + '}'


def from_pi_qew_list_to_tuple(pi_qew_list):
    result = []
    for i in range(len(pi_qew_list)):
        if type(pi_qew_list[i]) == list:
            result.append(from_pi_qew_list_to_tuple(pi_qew_list[i]))
        else:
            result.append(pi_qew_list[i])
    return tuple(result)


__author__ = 'pascal'
