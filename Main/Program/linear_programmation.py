__author__ = 'Gabriel'

'''
Contains the functions :

creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_1(pi_qwe_list, distance_matrix):
    given a pi_qwe_list like ['Q_node', ['P_node', [0], [1]], [2], [3]] and the associated distance_matrix 
    return the matrix M that represent the linear problem of an isotonic regression M . X <= b, 
    the sum of unknown value too minimise c, and the vector inequality b
    This function is to use if you want to use the l1 norm 
    
    Function calls:
        - creat_tuple_of_edges
        - creat_vector_c_for_l_1
        - creat_vector_inequality
    
creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_inf(pi_qwe_list, distance_to_use):
    similar to "creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_1" but for the l_inf norm 
    
        Function calls:
        - creat_tuple_of_edges
        - creat_vector_c_for_l_inf
        - creat_vector_inequality
    
modification_of_the_matrix_of_distance(vector_to_change_value, distance_to_use, current_graph):
    given the vector of the isotonic regression result, the matrix of distance that we aim to modify , and the graph 
    that we use to make the isotonic regression.
    modify the distance_to_use matrix directly so it return nothing

make_isotonic_for_l_1(pi_qwe_list, distance, print_matrix_bool=True)
    given a pi_qwe_list like ['Q_node', ['P_node', [0], [1]], [2], [3]] and a matrix of distance make the isotonic 
    regression and modify the distance matrix given the result of the isotonic regression with the l1 norm.
    
    Parameters:
        print_matrix_bool : If print_matrix_bool != True the distance obtain after the function is call 
        will not be print in the console 
    
    Function calls:
        - creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_1
        - modification_of_the_matrix_of_distance
        - linprog from scipy.optimize
        
        
make_isotonic_for_l_inf(pi_qwe_list, distance, print_matrix_bool=True)
    given a pi_qwe_list like ['Q_node', ['P_node', [0], [1]], [2], [3]] and a matrix of distance make the isotonic 
    regression and modify the distance matrix given the result of the isotonic regression with the l_inf norm.
    
    Parameters:
        print_matrix_bool : If print_matrix_bool != True the distance obtain after the function is call
         will not be print in the console but the matrix will still be modify
    
    Functions call:
        - creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_inf
        - modification_of_the_matrix_of_distance
        - linprog from scipy.optimize
     
make_round_on_matrix(matrix):
    given an matrix return a new matrix where each value correspond of the round value of the enter matrix.
    
    Function calls:
        - make_round
   
change_format_of_pi_qwe_list(list1):
    Given a pi_qwe_list like ['Q_node', ['P_node', 0, 1] , 2, 3]  
    return pi_qwe_list with bracket like ['Q_node', ['P_node', [0], [1]], [2], [3]] 

make_isotonic_regression_for_l2(pi_qwe_list, distance_matrix, print_matrix_bool=True):
    given a pi_qwe_list like ['Q_node', ['P_node', [0], [1]], [2], [3]] and a matrix of distance make the isotonic 
    regression and modify the distance matrix given the result of the isotonic regression with the l_2 norm.
    
    Parameters:
        print_matrix_bool : If print_matrix_bool != True the distance obtain after the function is call 
        will not be print in the console but the matrix will still be modify
    
    Function calls:
        - creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_2
        - modification_of_the_matrix_of_distance 
        - function_to_minimise
        - creat_lower_bound_vector_for_l_2_norm
        - creat_c_vector_for_l_2_norm
        - minimize from scipy.optimize
'''

from Main.Program.data import Data, taking_only_coordinates
from scipy.optimize import linprog, minimize, LinearConstraint
from math import ceil, floor
import numpy as np


def creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_1(pi_qwe_list, distance_matrix):
    data_to_use = Data(pi_qwe_list, distance_matrix, norme=1)
    graph = data_to_use.graph
    edge_list = creat_tuple_of_edges(graph)
    position_vector = taking_only_coordinates(data_to_use.position_vector)
    weight_vector = taking_only_coordinates(data_to_use.weight_vector)

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
    data_to_use = Data(pi_qwe_list, distance_to_use, norme='inf')
    edge_list = creat_tuple_of_edges(data_to_use.graph)
    position_vector = taking_only_coordinates(data_to_use.position_vector)
    weight_vector = taking_only_coordinates(data_to_use.weight_vector)
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

    return matrix, creat_vector_c_for_l_inf(len(weight_vector)), creat_vector_inequality(position_vector,
                                                                                         len(edge_list))


def creat_tuple_of_edges(graph_to_use, current_list=None):
    if current_list is None:
        current_list = []
    if graph_to_use.is_leaf():
        return current_list
    for neighbors in graph_to_use.neighbors:
        if [(graph_to_use.key, neighbors.key)] not in current_list:
            if [(neighbors.key, graph_to_use.key)] not in current_list:
                current_list += [(graph_to_use.key, neighbors.key)]
    for neighbors in graph_to_use.neighbors:
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


def creat_vector_inequality(position_vector, len_edge_list_vector):
    vector_inequality = np.zeros(2 * len(position_vector) + len_edge_list_vector)
    for index in range(0, 2 * len(position_vector), 2):
        vector_inequality[index] = - position_vector[int(index / 2)]
        vector_inequality[index + 1] = position_vector[int(index / 2)]
    return vector_inequality


def modification_of_the_matrix_of_distance(vector_to_change_value, distance_to_use, current_graph):
    robinson_dissimilarity = distance_to_use
    current_key = current_graph.key - 1
    if current_graph.is_leaf():
        return robinson_dissimilarity
    if current_graph.is_qwe_node():
        represent1 = current_graph.represents[0].points
        represent2 = current_graph.represents[1].points
        for n1 in represent1:
            for n2 in represent2:
                if n1 != n2:
                    robinson_dissimilarity[n1][n2] = vector_to_change_value[current_key]
                    robinson_dissimilarity[n2][n1] = vector_to_change_value[current_key]
            robinson_dissimilarity = modification_of_the_matrix_of_distance(vector_to_change_value,
                                                                            robinson_dissimilarity,
                                                                            current_graph.neighbors[0])
            robinson_dissimilarity = modification_of_the_matrix_of_distance(vector_to_change_value,
                                                                            robinson_dissimilarity,
                                                                            current_graph.neighbors[1])

    if current_graph.is_pi_node():
        for points1 in current_graph.points:
            for points2 in current_graph.points:
                if points1 != points2:
                    robinson_dissimilarity[points1][points2] = vector_to_change_value[current_key]
                    robinson_dissimilarity[points2][points1] = vector_to_change_value[current_key]

        for neighbors in current_graph.neighbors:
            robinson_dissimilarity = modification_of_the_matrix_of_distance(vector_to_change_value,
                                                                            robinson_dissimilarity, neighbors)

    return robinson_dissimilarity


def make_isotonic_for_l_1(pi_qwe_list, distance, print_matrix_bool=True):
    data_to_use = Data(pi_qwe_list, distance, norme=1)
    a_ineq, c, b_ineq = creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_1(pi_qwe_list, distance)
    res_no_bounds = linprog(c, A_ub=a_ineq, b_ub=b_ineq, method='interior-point')
    if print_matrix_bool:
        print(modification_of_the_matrix_of_distance(res_no_bounds['x'], distance, data_to_use.graph))
    else:
        modification_of_the_matrix_of_distance(res_no_bounds['x'], distance, data_to_use.graph)


def make_isotonic_for_l_inf(pi_qwe_list, distance, print_matrix_bool=True):
    graph = Data(pi_qwe_list, distance, norme='inf').graph
    a_ineq, c, b_ineq = creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_inf(pi_qwe_list, distance)
    res_no_bounds = linprog(c, A_ub=a_ineq, b_ub=b_ineq, method='interior-point')
    if print_matrix_bool:
        print(modification_of_the_matrix_of_distance(res_no_bounds['x'], distance, graph))
    else:
        modification_of_the_matrix_of_distance(res_no_bounds['x'], distance, graph)


def make_round(value):
    ceiling = ceil(value) - value
    if abs(ceiling - 0.5) <= 0.0005:
        new_value = int(value) + 0.5
        return new_value
    elif ceiling < 0.5:
        return ceil(value)
    elif ceiling > 0.5:
        return floor(value)


def make_round_l_2_norm(value):
    ceiling = ceil(value) - value
    flr = value - floor(value)
    if ceiling <= 0.25:
        return ceil(value)
    elif flr <= 0.25:
        return floor(value)
    else:
        return value


def make_round_on_matrix(matrix):
    for row_index in range(len(matrix)):
        for value_index in range(len(matrix[row_index])):
            matrix[row_index][value_index] = make_round(matrix[row_index][value_index])


def make_round_on_matrix_for_l_2_norm(matrix):
    for row_index in range(len(matrix)):
        for value_index in range(len(matrix[row_index])):
            matrix[row_index][value_index] = make_round_l_2_norm(matrix[row_index][value_index])


def change_format_of_pi_qwe_list(list1):
    list_to_return = list1
    for index in range(len(list_to_return)):
        if type(list_to_return[index]) == list:
            list_to_return[index] = change_format_of_pi_qwe_list(list_to_return[index])
        if (type(list_to_return[index]) != str) and (type(list_to_return[index]) != list):
            list_to_return[index] = [list_to_return[index]]
    return list_to_return


def print_matrix(matrix):
    print('\n')
    for row in matrix:
        print(row)
    print('\n')


def creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_2(pi_qwe_list, distance_matrix):
    data_to_use = Data(pi_qwe_list, distance_matrix, norme=2)
    edge_list = creat_tuple_of_edges(data_to_use.graph)
    position_vector = taking_only_coordinates(data_to_use.position_vector)

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

    return matrix, creat_vector_inequality(position_vector, len(edge_list))


def make_isotonic_regression_for_l2(pi_qwe_list, distance_matrix, print_matrix_bool=True):
    data_to_use = Data(pi_qwe_list, distance_matrix, norme=2)
    matrix_of_inequality_and_vector_b = creat_matrix_of_inequality_vector_c_and_vector_inequality_for_l_2(
        pi_qwe_list, distance_matrix)
    posistion_vector = taking_only_coordinates(data_to_use.position_vector)
    weight_vector = taking_only_coordinates(data_to_use.weight_vector)

    lower_bound = creat_lower_bound_vector_for_l_2_norm(len(matrix_of_inequality_and_vector_b[0]))

    x = creat_c_vector_for_l_2_norm(len(matrix_of_inequality_and_vector_b[0][0]), posistion_vector)

    linear_constraint = LinearConstraint(matrix_of_inequality_and_vector_b[0], lower_bound,
                                         matrix_of_inequality_and_vector_b[1])
    res = minimize(function_to_minimise, x, method='trust-constr', constraints=linear_constraint,
                   args=(weight_vector, posistion_vector))
    # in that specific case the PEP8 is not respected but this is a bug see the constraints section at
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html

    if print_matrix_bool:
        print(modification_of_the_matrix_of_distance(res.x, distance_matrix,
                                                     data_to_use.graph))
    else:
        modification_of_the_matrix_of_distance(res.x, distance_matrix, data_to_use.graph)


def creat_c_vector_for_l_2_norm(len_of_matrix_inequality_row, position_vector):
    c = np.ndarray(len_of_matrix_inequality_row)

    for index in range(len_of_matrix_inequality_row):
        if index < len(position_vector):
            c[index] = position_vector[index]
        else:
            c[index] = 0

    return c


def creat_lower_bound_vector_for_l_2_norm(len_of_inequality_matrix_columns):
    lower_bound = np.zeros(len_of_inequality_matrix_columns)

    for i in range(len(lower_bound)):
        lower_bound[i] = -np.inf

    return lower_bound


def function_to_minimise(x, weight, pos):
    value = 0
    for value_index in range(int(len(x) / 2)):
        value += np.float64(weight[value_index]) * (np.float64(abs(x[value_index] - pos[value_index]))) ** 1 / 2
    return value
