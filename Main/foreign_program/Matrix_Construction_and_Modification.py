__author__ = 'pascal'

"""
Contains the functions:

geographic_distance(nb_points, breadth, approximation, confusion):
    Given the 4 parameters "nb_points", "breadth", "approximation" and "confusion", 
    Returns a couple ("distance", "pi_qew_tree") on "nb_points" points
    Works as follows :
        1 : randomly generates "nb_points" points in a square x_max X y_max, where
                x_max = 10 X "nb_points"
                y_max = x_max X "breadth" / 100
        2 : builds the L_1 distance between these points
            divides this distance by "approximation" and round it.
            the result of this is "distance"
        3 : builds the PQ-tree "pi_qew_tree" that follows the x-order of the points. 
            the root of "pi_qe_tree" is a Q-node
            if a consecutive set of points dwells on an x-interval smaller than "confusion" separated from other points
                by more than "confusion", then these points are grouped under a P-node. So, if "confusion" is very 
                small or great, "pi_qew_tree" is flat. "confusion" = 10-15 seems to create the greatest number of 
                P-nodes.
    If "breadth" is small, "distance" is close to be Robinson and "pi_qew_tree" nearly represents its compatible 
            permutations


add_uniform_noise(distance, noise_value)
add_non_uniform_noise(distance, percent_of_changed, noise_value)
    these functions add noise to the matrix "distance"

empty_matrix(size)
    returns a square "size" x "size" 0 matrix

make_symmetric(distance)
    Given a SQUARE matrix "distance". if i != j and distance[i][j] == 0, then distance[i][j] <- distance[j][i]

completion_lower_triangle_into_distance(low_triangle)
    Given the lower part (INCLUDING THE DIAGONAL) of a SQUARE matrix "low_triangle",
    completes it into a symmetric matrix
    USES make_symmetric

completion_upper_triangle_into_distance(upper_triangle)
    Given the upper part (INCLUDING THE DIAGONAL) of a SQUARE matrix "upper_triangle",
    completes it into a symmetric matrix
    USES make_symmetric

from_attribute_value_matrix_to_distance_continuous(matrix)
from_attribute_value_matrix_to_distance_binary(matrix)
    returns a dissimilarity based on the attribute-value matrix "matrix"

standard_distance_construction_from_pi_qew_tree(tree, size)
    given a PQ-tree "tree" on the set X = {0, .., "size" -1}, returns a 'standard' Robinson dissimilarity on X
    which admits "tree" as its PQ-tree.
    A node of a PQ-tree is a structure (implemented as a dictionary) whose description is given at the head of module
    "Basic_Function_for_PQ-Trees"


robinson_matrix_construction(size, hazard):
    returns a Robinson dissimilarity on the set {0,.. "size" - 1}
    the parameter "hazard" determines the proportion of equal values in the dissimilarity

exemple_du_papier()
quasi_exemple_du_papier()
    two particular examples of Robinson dissimilarities

distance_vartan()
    a non Robinson dissimilarity
"""

import random
import math

from Main.foreign_program.Diverse_Functions import suppression_of_identical_lines
from Main.foreign_program.Diverse_Functions import sort_indices_by_values

from Main.foreign_program.basic_fonctions_for_PQ_trees import update_father_and_leaf_sets
from Main.foreign_program.basic_fonctions_for_PQ_trees import depth

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

########################################################################################################################


def geographic_distance(nb_points, breadth, approximation, confusion):
    the_points = geographic_point_generation(nb_points, breadth)
    distance = geographic_distance_construction(the_points, approximation)
    pi_qew_tree = geographic_pi_qew_tree_construction(the_points, confusion)
    return distance, pi_qew_tree


def geographic_pi_qew_tree_construction(the_points, confusion):
    nb = len(the_points)
    x_values = [point[0] for point in the_points]
    indices = list(range(nb))
    sort_indices_by_values(indices, x_values)
    indices = geographic_points_repartition(indices, x_values, nb, confusion)
    return concrete_pi_qew_tree_construction(indices)


def concrete_pi_qew_tree_construction(indices):
    result = [Q_NODE]
    for index in indices:
        if type(index) is list:
            result.append([P_NODE] + index)
        else:
            result.append(index)
    return result


def geographic_points_repartition(indices, x_values, nb, confusion):
    holes_indices = hole_indices_construction(x_values, nb, confusion)
    if len(holes_indices) == 1:
        return indices
    result = []
    holes_indices.append(nb)
    for i in range(1, len(holes_indices)):
        zone_top, zone_bottom = holes_indices[i] - 1, holes_indices[i - 1]
        if zone_top != zone_bottom and x_values[zone_top] - x_values[zone_bottom] < confusion:
            result.append(indices[zone_bottom: zone_top + 1])
        else:
            result.extend(indices[zone_bottom: zone_top + 1])
    return result


def hole_indices_construction(x_values, nb, confusion):
    result = [0]
    for index in range(1, nb):
        if x_values[index] - x_values[index - 1] > confusion:
            result.append(index)
    return result


def geographic_distance_construction(the_points, approximation):
    nb_pt = len(the_points)
    the_distance = []
    for i in range(nb_pt):
        line = []
        for j in range(nb_pt):
            line.append(approximate_l1_distance(the_points[i], the_points[j], approximation))
        the_distance.append(line)
    return the_distance


def approximate_l1_distance(pt_1, pt_2, approximation):
    if pt_1 == pt_2:
        return 0
    l1_distance = math.fabs(pt_1[0] - pt_2[0]) + math.fabs(pt_1[1] - pt_2[1])
    return 1 + math.floor(l1_distance / approximation)


def geographic_point_generation(nb_points, breadth):
    x_max = 10 * nb_points
    y_max = math.ceil(nb_points * breadth / 10)
    the_points = set([])
    while len(the_points) < nb_points:
        the_points.add((random.randrange(x_max), random.randrange(y_max)))
    return list(the_points)

# ############################################# FIN geographic_distance ############################################## #


def add_uniform_noise(distance, noise_value):
    size = len(distance)
    for i in range(size):
        for j in range(i + 1, size):
            distance[i][j] += random.randint(0, noise_value)
            distance[j][i] = distance[i][j]


def add_non_uniform_noise(distance, percent_of_changed, noise_value):
    size = len(distance)
    for i in range(size):
        for j in range(i + 1, size):
            if random.randint(0, 100) < percent_of_changed:
                distance[i][j] += random.randint(noise_value // 2, noise_value)
                distance[j][i] = distance[i][j]


def empty_matrix(size):
    matrix = []
    for i in range(size):
        matrix.append([0] * size)
    return matrix


def make_symmetric(distance):
    size = len(distance)
    for i in range(size):
        for j in range(size):
            if distance[i][j] == 0:
                distance[i][j] = distance[j][i]


def completion_lower_triangle_into_distance(low_triangle):
    max_length = len(low_triangle[-1])
    for i in range(len(low_triangle)):
        line_end = [0] * (max_length - len(low_triangle[i]))
        low_triangle[i] = low_triangle[i] + line_end
    make_symmetric(low_triangle)


def completion_upper_triangle_into_distance(upper_triangle):
    max_length = len(upper_triangle[1])
    for i in range(len(upper_triangle)):
        line_beginning = [0] * (max_length - len(upper_triangle[i]))
        upper_triangle[i] = line_beginning + upper_triangle[i]
    make_symmetric(upper_triangle)


def from_attribute_value_matrix_to_distance_continuous(matrix):
    matrix = suppression_of_identical_lines(matrix)
    size = len(matrix)
    distance = empty_matrix(size)
    for i in range(size):
        for j in range(i + 1, size):
            for column in range(matrix[i]):
                distance[i][j] += abs(matrix[i][column] - matrix[j][column])
            distance[j][i] = distance[i][j]
    return distance


def from_attribute_value_matrix_to_distance_binary(matrix):
    matrix = suppression_of_identical_lines(matrix)
    size = len(matrix)
    distance = empty_matrix(size)
    for i in range(size):
        for j in range(i + 1, size):
            for column in range(matrix[i]):
                if matrix[i][column] != matrix[j][column]:
                    distance[i][j] += 1
            distance[j][i] = distance[i][j]
    return distance


#######################################################################################################################

def standard_distance_from_pi_qew_tree(tree, size):
    if tree is not None and tree[PORQ] != LEAF:
        distance = empty_matrix(size)
        update_father_and_leaf_sets(tree)
        distance_update_from_pi_qew_tree(tree, distance)
        make_symmetric(distance)
        return distance


def distance_update_from_pi_qew_tree(tree, distance):
    if tree is not None and tree[PORQ] != LEAF:
        node = tree[CADET]
        while node is not None:
            distance_update_from_pi_qew_tree(node, distance)
            node = node[GD_FRERE]
        height = 2 * depth(tree)
        if tree[PORQ] == P_NODE:
            distance_update_for_pi_node(tree, distance, height)
        elif tree[PORQ] == Q_NODE:
            distance_update_for_qew_node(tree, distance, height)


def distance_update_for_pi_node(tree, distance, height):
    current_node = tree[CADET]
    while current_node is not None:
        current_set = current_node[LEAF_SET]
        other_node = current_node[GD_FRERE]
        while other_node is not None:
            for i in current_set:
                for j in other_node[LEAF_SET]:
                    distance[i][j] = height
            other_node = other_node[GD_FRERE]
        current_node = current_node[GD_FRERE]


def distance_update_for_qew_node(tree, distance, height):
    current_node = tree[CADET]
    while current_node is not None:
        current_set = current_node[LEAF_SET]
        other_node = current_node[GD_FRERE]
        if other_node is not None:
            for i in current_set:
                for j in other_node[LEAF_SET]:
                    distance[i][j] = height - 1
            other_node = other_node[GD_FRERE]
        while other_node is not None:
            for i in current_set:
                for j in other_node[LEAF_SET]:
                    distance[i][j] = height
            other_node = other_node[GD_FRERE]
        current_node = current_node[GD_FRERE]

#######################################################################################################################


#######################################################################################################################

def robinson_matrix_construction(size, hazard):
    vector = list(range(size))
    random.shuffle(vector)
    distance = empty_matrix(size)
    robinson_filling(distance, vector, hazard)
    return distance


def robinson_filling(distance, vector, hazard):
    size = len(vector)
    for diagonal_nb in range(1, size):
        for i in range(size - diagonal_nb):
            j = i + diagonal_nb
            value_on_left = distance[vector[i]][vector[j - 1]]
            value_under = distance[vector[i + 1]][vector[j]]
            value = max(value_on_left, value_under) + random_modification(hazard)
            distance[vector[i]][vector[j]] = value
    make_symmetric(distance)
    suppression_of_zeros(distance)


def random_modification(hazard):
    random_nb = random.randint(0, abs(hazard))
    if hazard < 0:
        random_nb = random_nb // abs(hazard)
    return random_nb


def suppression_of_zeros(distance):
    size = len(distance)
    for i in range(size):
        for j in range(size):
            if i != j:
                distance[i][j] += 1

#######################################################################################################################


def exemple_du_papier():
    mat = [[0, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
           [0,  0,  9,  2, 11,  6, 11,  6,  6,  9, 11,  6, 11,  6,  5, 11, 11,  9, 11,  6],
           [0,  0,  0,  9, 11,  2, 11,  3,  6,  1, 11,  6, 11,  6,  9, 11, 11,  1, 11,  3],
           [0,  0,  0,  0, 11,  6, 11,  6,  6,  9, 11,  6, 11,  6,  1, 11, 11,  9, 11,  6],
           [0,  0,  0,  0,  0, 11,  8, 11, 11, 11,  8, 11,  8, 11, 11,  1,  8, 11,  2, 11],
           [0,  0,  0,  0,  0,  0, 11,  3,  4,  2, 11,  4, 11,  4,  6, 11, 11,  2, 11,  1],
           [0,  0,  0,  0,  0,  0,  0, 11, 11, 11,  1, 11,  5, 11, 11,  6,  3, 11,  6, 11],
           [0,  0,  0,  0,  0,  0,  0,  0,  4,  3, 11,  4, 11,  4,  6, 11, 11,  3, 11,  2],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  5, 11,  1, 11,  3,  4, 11, 11,  5, 11,  4],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  5, 11,  6,  9, 11, 11,  1, 11,  3],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  5, 11, 11,  7,  2, 11,  6, 11],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  2,  4, 11, 11,  5, 11,  4],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11, 11,  2,  5, 11,  1, 11],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  4, 11, 11,  6, 11,  4],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11, 11,  9, 11,  6],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7, 11,  1, 11],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  7, 11],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11,  3],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
           [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]
    make_symmetric(mat)
    return mat


def quasi_exemple_du_papier():
    mat = exemple_du_papier()
    for line in mat:
        line.append(22)
    n = len(mat)
    mat.append([22] * n)
    mat[-1].append(0)
    return mat


def distance_vartan():
    distance = [[0,     1,     5,     5,     6,     7,    10,     6,     7,     7],
                [0,     0,     4,     6,     5,     8,    11,     7,     8,     8],
                [0,     0,     0,     6,     9,     8,     9,     7,     8,     8],
                [0,     0,     0,     0,     7,     6,     9,     5,     8,     8],
                [0,     0,     0,     0,     0,     5,    12,    10,    11,    11],
                [0,     0,     0,     0,     0,     0,     9,     9,     8,     8],
                [0,     0,     0,     0,     0,     0,     0,     4,     5,     9],
                [0,     0,     0,     0,     0,     0,     0,     0,     5,     7],
                [0,     0,     0,     0,     0,     0,     0,     0,     0,     4],
                [0,     0,     0,     0,     0,     0,     0,     0,     0,     0]]
    make_symmetric(distance)
    return distance
