__author__ = 'Gabriel'

from Main.Program.Constant import *
from Main.foreign_program.PQ_Tree_To_Graph_Transformation import \
    from_pi_qew_tree_to_basic_graph_with_position_and_weight


def taking_only_coordinates(vector):
    coordinates = []
    for tuples in vector:
        coordinates += [tuples[1]]
    return coordinates


class Data:
    def __init__(self, pi_qwe_list, distance, norme):
        graph_with_position_and_weight = from_pi_qew_tree_to_basic_graph_with_position_and_weight \
            (pi_qwe_list, distance, norme)
        self.graph = Graph(graph_with_position_and_weight[0])
        self.position_vector = graph_with_position_and_weight[1]
        self.weight_vector = graph_with_position_and_weight[2]


def creat_position_vector_for_l_inf(pq_graph, position_vector=None):
    if position_vector is None:
        position_vector = []
    min_max = (pq_graph.average_distance[2] + pq_graph.average_distance[3]) / 2
    if pq_graph.type.is_leaf():
        if (pq_graph.key, min_max) in position_vector:
            return position_vector
        else:
            position_vector.append((pq_graph.key, 0))
            return position_vector
    else:
        if (pq_graph.key, min_max) not in position_vector:
            position_vector.append((pq_graph.key, min_max))

        if pq_graph.is_pi_node():
            for neighbors in pq_graph.neighbors:
                pq_graph.creat_position_vector_for_l1(neighbors, position_vector)
        else:
            pq_graph.creat_position_vector_for_l_inf(pq_graph.neighbors[0], position_vector)
            pq_graph.creat_position_vector_for_l_inf(pq_graph.neighbors[1], position_vector)
        return position_vector


def creat_weight_vector(pq_graph, weight_vector=None):
    if weight_vector is None:
        weight_vector = []
    if pq_graph.is_leaf():
        if (pq_graph.key, 1) not in weight_vector:
            weight_vector.append((pq_graph.key, pq_graph.average_distance[1]))
            return weight_vector
    else:
        weight_vector.append((pq_graph.key, pq_graph.average_distance[1]))
        if pq_graph.is_pi_node():
            for neighbors in pq_graph.neighbors:
                pq_graph.creat_position_vector_for_l1(neighbors, weight_vector)
        else:
            pq_graph.creat_position_vector_for_l2(pq_graph.neighbors[0], weight_vector)
            pq_graph.creat_position_vector_for_l2(pq_graph.neighbors[1], weight_vector)
        return weight_vector


def creat_position_vector_for_l2(pq_graph, position_vector=None):
    if position_vector is None:
        position_vector = []
    mean = pq_graph.average_distance[0] / pq_graph.average_distance[1]
    if pq_graph.is_leaf():
        if (pq_graph.key, mean) in position_vector:
            return position_vector
        else:
            position_vector.append((pq_graph.key, 0))
            return position_vector
    else:
        if (pq_graph.key, mean) not in position_vector:
            position_vector.append((pq_graph.key, mean))
        if pq_graph.is_pi_node():
            for neighbors in pq_graph.neighbors:
                pq_graph.creat_position_vector_for_l1(neighbors, position_vector)
        else:
            pq_graph.creat_position_vector_for_l2(pq_graph.neighbors[0], position_vector)
            pq_graph.creat_position_vector_for_l2(pq_graph.neighbors[1], position_vector)
        return position_vector


def creat_position_vector_for_l1(pq_graph, position_vector=None):
    if position_vector is None:
        position_vector = []
    if pq_graph.is_leaf():
        if (pq_graph.key, pq_graph.average_distance[4]) in position_vector:
            return position_vector
        else:
            position_vector.append((pq_graph.key, 0))
            return position_vector
    else:
        if (pq_graph["leaf"], pq_graph.average_distance[4]) not in position_vector:
            position_vector.append((pq_graph.key, pq_graph.average_distance[4]))

        if pq_graph.is_pi_node():
            for neighbors in pq_graph.neighbors:
                pq_graph.creat_position_vector_for_l1(neighbors, position_vector)
        else:
            pq_graph.creat_position_vector_for_l1(pq_graph.neighbors[0], position_vector)
            pq_graph.creat_position_vector_for_l1(pq_graph.neighbors[1], position_vector)
        return position_vector


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
