__author__ = 'Gabriel'

from Main.Program.Constant import *
from Main.foreign_program.PQ_Tree_To_Graph_Transformation import \
    from_pi_qew_tree_to_basic_graph_with_position_and_weight

from Main.foreign_program.Diverse_Functions import distance_between_matrices
from Main.foreign_program.Matrix_Construction_and_Modification import geographic_distance

from Main.foreign_program.Matrix_Construction_and_Modification import standard_distance_from_pi_qew_tree, \
    add_non_uniform_noise, add_uniform_noise

from Main.foreign_program.type_conversions_for_PQ_trees import from_pi_qew_tree_to_list
from Main.foreign_program.Global_Functions_for_PQ_Trees import random_generation_of_pi_qew_tree


class Data:
    def __init__(self, pi_qwe_list, distance, norme):
        graph_with_position_and_weight = from_pi_qew_tree_to_basic_graph_with_position_and_weight \
            (pi_qwe_list, distance, norme)
        self.graph = Graph(graph_with_position_and_weight[0])
        self.position_vector = graph_with_position_and_weight[1]
        self.weight_vector = graph_with_position_and_weight[2]


def taking_only_coordinates(vector):
    coordinates = []
    for tuples in vector:
        coordinates += [tuples[1]]
    return coordinates


class Graph():
    def __init__(self, graph_to_transform):

        self.type = graph_to_transform[TYPE]
        self.key = graph_to_transform[KEY]
        self.points = graph_to_transform[POINTS]
        self.average_distance = graph_to_transform[AVERAGE_DISTANCE]

        if graph_to_transform[TYPE] == LEAF:
            self.neighbors = graph_to_transform[NEIGHBORS]

        elif graph_to_transform[TYPE] == Q_NODE:
            self.neighbors = []
            self.represents = []
            for represents in graph_to_transform[REPRESENTS]:
                self.represents += [Graph(represents)]
            for neighbors in graph_to_transform[NEIGHBORS]:
                self.neighbors += [Graph(neighbors)]
        else:
            self.neighbors = []
            for neighbors in graph_to_transform[NEIGHBORS]:
                self.neighbors += [Graph(neighbors)]

    def is_qwe_node(self):
        if self.type == Q_NODE:
            return True
        else:
            return False

    def is_leaf(self):
        if self.type == LEAF:
            return True
        else:
            return False

    def is_pi_node(self):
        if self.type == P_NODE:
            return True
        else:
            return False


def facade_distance_between_matrices(m1, m2):
    return distance_between_matrices(m1, m2)


def facade_geographic_distance(nb_points, breadth, approximation, confusion):
    return geographic_distance(nb_points, breadth, approximation, confusion)


def facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree):
    return standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)


def facade_add_non_uniform_noise(distance, percent_of_changed, noise_value):
    add_non_uniform_noise(distance, percent_of_changed, noise_value)


def facade_from_pi_qew_tree_to_list(tree_to_use):
    return from_pi_qew_tree_to_list(tree_to_use)


def facade_random_generation_of_pi_qew_tree(size, nb_of_intervals):
    return random_generation_of_pi_qew_tree(size, nb_of_intervals)


def facade_add_uniform_noise(noise_matrix, noise_value):
    add_uniform_noise(noise_matrix, noise_value)
