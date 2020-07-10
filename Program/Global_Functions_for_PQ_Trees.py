__author__ = 'pascal'

"""
Contains the functions:

lattice_inf(tree_1, tree_2, points)
    "tree_1" and "tree_2" are two PQ-trees defined on the same underlying set "points" (= [0, .. n-1]).
    Returns the inf of "tree_1 "and "tree_2" in the lattice of all PQ_trees on "points", i.e. the
    PQ-tree representing the largest set of permutations included in the intersection of the set of
    permutations represented by "tree_1" and the set of permutations represented by "tree_2".
    Returns None if this intersection is empty.
    USES FUNCTION "update_tree" FROM THE LIBRARY "booth_lueker"
         FUNCTION "minimal_subset_set_of" FROM LIBRARY "basic_fonctions_for_PQ_trees"

lattice_sup(tree_1, tree_2, points)
    "tree_1" and "tree_2" are two PQ-trees defined on the same underlying set "points" (= [0, .. n-1]).
    Returns the sup of "tree_1 "and "tree_2" in the lattice of all PQ_trees on "points", i.e. the
    PQ-tree representing the smallest set of permutations containing the set of
    permutations represented by "tree_1" and the set of permutations represented by "tree_2".
    USES FUNCTION "booth_and_lueker" FROM THE LIBRARY "booth_lueker"
         FUNCTION "characteristic_subset_set_of" FROM LIBRARY "basic_fonctions_for_PQ_trees"


lattice_distance_between_pi_qew_trees(tree_1, tree_2, points)
    "tree_1" and "tree_2" are two PQ-trees defined on the same underlying set "points" (= [0, .. n-1]).
    Returns a list of length 2 which contains two "distances" between tree_1 and tree_2.
    These distances are based on the lattice structure of teh set of all the PQ-trees on "points"
    See the code for the definition of these distances.
    USES FUNCTIONS "logarithm" AND "number_of_permutations_represented_by" FROM LIBRARY "Diverse_Functions"
         FUNCTION "minimal_subset_set_of" AND "number_of_permutations_represented_by"
            FROM LIBRARY "basic_fonctions_for_PQ_trees"


matrix_distance_between_pi_qew_trees(tree_1, tree_2, points)
    "tree_1" and "tree_2" are two PQ-trees defined on the same underlying set "points" (= [0, .. n-1]).
    Returns a list of length 3 which contains three "distances" between tree_1 and tree_2.
    These distances are based on comparison between 'standard' Robinson matrices having tree_1 and tree_2
    as PQ-trees (in order : L-infinite, L-1 and L-2).
    USES FUNCTION "standard_distance_from_pi_qew_tree" FROM LIBRARY "Matrix_Construction_and_Modification"


all_distances_between_pi_qew_trees(tree_1, tree_2, points):
    "tree_1" and "tree_2" are two PQ-trees defined on the same underlying set "points" (= [0, .. n-1]).
    returns the concatenation of lattice_distance_between_pi_qew_trees(tree_1, tree_2, points) and of
    matrix_distance_between_pi_qew_trees(tree_1, tree_2, points)


random_generation_of_pi_qew_tree(size, nb_of_intervals)
    returns a random PQ-tree on {0, .., "size" -1}, built with "nb_of_intervals" subsets
    USES FUNCTION "booth_and_lueker" FROM THE LIBRARY "booth_lueker"
         LIBRARY "random"

A node of a PQ-tree is a structure (implemented as a dictionary) whose description is given at the head of module
"Basic_Function_for_PQ-Trees"
Such a structure is not well printable.
To visualize a PQ-tree, use functions in module "Type_Conversions_for_PQ-Tree"
"""

import random

from booth_lueker import booth_and_lueker
from booth_lueker import update_tree

from basic_fonctions_for_PQ_trees import characteristic_subset_set_of
from basic_fonctions_for_PQ_trees import minimal_subset_set_of
from basic_fonctions_for_PQ_trees import number_of_permutations_represented_by

from Diverse_Functions import logarithm
from Diverse_Functions import distance_between_matrices

from Subset_construction import set_of_intervals_construction

from Matrix_Construction_and_Modification import standard_distance_from_pi_qew_tree


def lattice_inf(tree_1, tree_2, points):
    subsets_1 = minimal_subset_set_of(tree_1)
    subsets_2 = minimal_subset_set_of(tree_2)
    tree_max = tree_1
    subsets_min = subsets_2
    if len(subsets_1) < len(subsets_2):
        tree_max = tree_2
        subsets_min = subsets_1
    nb_accepted, nb_refused = 0, 0
    for subset in subsets_min:
        [nb_accepted, nb_refused, not_used] = update_tree(tree_max, subset, len(points), nb_accepted, nb_refused, [])
    if nb_refused == 0:
        return tree_max


def lattice_sup(tree_1, tree_2, points):
    if tree_1 is None:
        return tree_2
    if tree_2 is None:
        return tree_1
    subsets_1 = characteristic_subset_set_of(tree_1)
    subsets_2 = characteristic_subset_set_of(tree_2)
    subsets = list(subsets_1.intersection(subsets_2))
    return booth_and_lueker(subsets, points)[0]


def lattice_distance_between_pi_qew_trees(tree_1, tree_2, points):
    the_sup = lattice_sup(tree_1, tree_2, points)
    the_inf = lattice_inf(tree_1, tree_2, points)
    nb_sup = logarithm(number_of_permutations_represented_by(the_sup), 10)
    nb_inf = logarithm(number_of_permutations_represented_by(the_inf), 10)
    the_inf = lattice_inf(tree_1, tree_2, points)
    nb_sup_bis = len(minimal_subset_set_of(the_sup))
    nb_inf_bis = len(points)
    if the_inf is not None:
        nb_inf_bis = len(minimal_subset_set_of(the_inf))
    return [nb_sup - nb_inf, nb_inf_bis - nb_sup_bis]


def matrix_distance_between_pi_qew_trees(tree_1, tree_2, points):
    matrix_1 = standard_distance_from_pi_qew_tree(tree_1, len(points))
    matrix_2 = standard_distance_from_pi_qew_tree(tree_2, len(points))
    return distance_between_matrices(matrix_1, matrix_2)


def all_distances_between_pi_qew_trees(tree_1, tree_2, points):
    distance_by_lattice = lattice_distance_between_pi_qew_trees(tree_1, tree_2, points)
    distance_by_matrices = matrix_distance_between_pi_qew_trees(tree_1, tree_2, points)
    return distance_by_lattice + distance_by_matrices


def random_generation_of_pi_qew_tree(size, nb_of_intervals):
    points = list(range(size))
    random.shuffle(points)
    set_of_intervals = set_of_intervals_construction(points, nb_of_intervals)
    return booth_and_lueker(set_of_intervals, points)[0]
