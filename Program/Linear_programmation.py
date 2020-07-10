__author__ = 'Gabriel'

from Program.PQ_Tree_To_Graph_Transformation import from_pi_qew_tree_to_basic_graph_with_position_and_weight, \
    taking_only_coordinates
from Program.Constant import TYPE, P_NODE, Q_NODE, LEAF, KEY, NEIGHBORS, REPRESENTS, POINTS

from scipy.optimize import linprog
import numpy as np


def creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_1(pi_qwe_list, distance_matrix):
    graph_to_use, position_vector, weight_vector = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list,
                                                                                                        distance_matrix,
                                                                                                            norme=1)
    edge_list = creat_tuple_of_edges(graph_to_use)
    position_vector = taking_only_coordinates(position_vector)
    weight_vector = taking_only_coordinates(weight_vector)

    matrix = np.zeros((2 * len(position_vector) + len(edge_list), 2 * len(position_vector)))
    len_of_vector = len(position_vector)
    index_of_lenght = 0
    for index_of_height in range(0, 2 * len_of_vector, 2):
        matrix[index_of_height][index_of_lenght] = -1
        matrix[index_of_height][index_of_lenght + len_of_vector] = -1
        matrix[index_of_height + 1][index_of_lenght] = 1
        matrix[index_of_height + 1][index_of_lenght + len_of_vector] = -1
        index_of_lenght += 1

    for index_of_height in range(len(edge_list)):
        matrix[2 * len_of_vector + index_of_height][edge_list[index_of_height][1] - 1] = 1
        matrix[2 * len_of_vector + index_of_height][edge_list[index_of_height][0] - 1] = -1

    return matrix, creat_vector_c_for_l_1(weight_vector), creat_vector_inequality(position_vector, len(edge_list))


def creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_inf(pi_qwe_list, distance_to_use):
    graph_to_use, position_vector, weight_vector = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list,
                                                                                                        distance_to_use,
                                                                                                            norme='inf')
    edge_list = creat_tuple_of_edges(graph_to_use)
    position_vector = taking_only_coordinates(position_vector)
    weight_vector = taking_only_coordinates(weight_vector)
    len_of_vector = len(position_vector)
    matrix = np.zeros((2 * len_of_vector + len(edge_list), len_of_vector + 1))
    index_of_lenght = 0
    for index_of_height in range(0, 2 * len_of_vector, 2):
        matrix[index_of_height][index_of_lenght] = -1
        matrix[index_of_height][len_of_vector] = -1
        matrix[index_of_height + 1][index_of_lenght] = 1
        matrix[index_of_height + 1][len_of_vector] = -1
        index_of_lenght += 1

    for index_of_height in range(len(edge_list)):
        matrix[2 * len_of_vector + index_of_height][edge_list[index_of_height][1] - 1] = 1
        matrix[2 * len_of_vector + index_of_height][edge_list[index_of_height][0] - 1] = -1

    return matrix, creat_vector_c_for_l_inf(len_of_vector), creat_vector_inequality(position_vector, len(edge_list))


def creat_tuple_of_edges(graph_to_use, current_list=None):
    if current_list is None:
        current_list = []
    if graph_to_use[TYPE] == LEAF:
        return current_list
    for neighbors in graph_to_use[NEIGHBORS]:
        if [(graph_to_use[KEY], neighbors[KEY])] not in current_list:
            if [(neighbors[KEY], graph_to_use[KEY])] not in current_list:
                current_list += [(graph_to_use[KEY], neighbors[KEY])]
    for neighbors in graph_to_use[NEIGHBORS]:
        creat_tuple_of_edges(neighbors, current_list)
    return current_list


def creat_vector_c_for_l_inf(len_vector_position):
    c_vector = np.zeros(len_vector_position + 1)
    c_vector[len_vector_position] = 1
    return c_vector


def creat_vector_c_for_l_1(weight_vector):
    weight_vector_on_np = np.array(weight_vector)
    zero = np.zeros(len(weight_vector))
    c_vector = np.append(zero, weight_vector_on_np)
    return c_vector


def creat_vector_inequality(position_vector, len_weight_vector):
    vector_inequality = np.zeros(2 * len(position_vector) + len_weight_vector)
    for index in range(0, 2 * len(position_vector), 2):
        vector_inequality[index] = - position_vector[int(index / 2)]
        vector_inequality[index + 1] = position_vector[int(index / 2)]
    return vector_inequality


def modification_of_the_matrix_of_distance(vector_to_change_value, distance_to_use, current_graph):
    robinson_dissimilarity = distance_to_use
    current_key = current_graph[KEY] - 1
    if current_graph[TYPE] == LEAF:
        return robinson_dissimilarity
    if current_graph[TYPE] == Q_NODE:
        represent1 = current_graph[REPRESENTS][0][POINTS]
        represent2 = current_graph[REPRESENTS][1][POINTS]
        for n1 in represent1:
            for n2 in represent2:
                if n1 != n2:
                    robinson_dissimilarity[n1][n2] = vector_to_change_value[current_key]
                    robinson_dissimilarity[n2][n1] = vector_to_change_value[current_key]
            robinson_dissimilarity = modification_of_the_matrix_of_distance(vector_to_change_value,
                                                                            robinson_dissimilarity,
                                                                            current_graph[NEIGHBORS][0])
            robinson_dissimilarity = modification_of_the_matrix_of_distance(vector_to_change_value,
                                                                            robinson_dissimilarity,
                                                                            current_graph[NEIGHBORS][1])

    if current_graph[TYPE] == P_NODE:
        for points1 in current_graph[POINTS]:
            for points2 in current_graph[POINTS]:
                if points1 != points2:
                    robinson_dissimilarity[points1][points2] = vector_to_change_value[current_key]
                    robinson_dissimilarity[points2][points1] = vector_to_change_value[current_key]

        for neighbors in current_graph[NEIGHBORS]:
            robinson_dissimilarity = modification_of_the_matrix_of_distance(vector_to_change_value,
                                                                            robinson_dissimilarity, neighbors)

    return robinson_dissimilarity


distance_0 = [[0, 1, 1, 3, 3],
              [1, 0, 1, 1, 3],
              [1, 1, 0, 1, 3],
              [3, 1, 1, 0, 3],
              [3, 3, 3, 3, 0]]

distance_0_bis = [[0, 1.00, 1.00, 2.99, 2.99],
                  [1.00, 0, 1.00, 1.00, 2.99],
                  [1.00, 1.00, 0, 1.00, 2.99],
                  [2.99, 1.00, 1.00, 0, 2.99],
                  [2.99, 2.99, 2.99, 2.99, 0]]

distance_0_bis_inf =  [[0, 1.0000000000643283, 1.0000000000643283, 3.0000000000352576, 3.0000000000534484],
                       [1.0000000000643283, 0, 0.9999999999610419, 1.0000000000643294, 3.0000000000534484],
                       [1.0000000000643283, 0.9999999999610419, 0, 1.0000000000643294, 3.0000000000534484],
                       [3.0000000000352576, 1.0000000000643294, 1.0000000000643294, 0, 3.0000000000534484],
                       [3.0000000000534484, 3.0000000000534484, 3.0000000000534484, 3.0000000000534484, 0]]


def make_isotonic(list,distance):

    graph = from_pi_qew_tree_to_basic_graph_with_position_and_weight(list, distance)[0]
    A_ineq, c, B_ineq = creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_inf(list, distance)
    res_no_bounds = linprog(c, A_ub=A_ineq, b_ub=B_ineq, method='interior-point')
    print(modification_of_the_matrix_of_distance(res_no_bounds['x'], distance, graph))
