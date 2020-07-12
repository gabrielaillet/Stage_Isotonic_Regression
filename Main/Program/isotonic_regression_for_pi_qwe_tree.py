__author__ = 'Gabriel'

import matplotlib.pyplot as plt
import numpy as np
from sklearn.isotonic import IsotonicRegression
from Main.Program.explotation_isotonique_regression import study_isotonic_regression_l2
from Main.Program.pq_tree_preparation_isotonique import creat_weight_vector, creat_position_vector_for_l2
from Main.foreign_program.PQ_Tree_To_Graph_Transformation import from_pi_qew_tree_to_basic_graph_with_position_and_weight, \
    taking_only_coordinates
from Main.foreign_program.Constant import *



# #############################################################################
# Fit IsotonicRegression and LinearRegression models
def make_isotonic_regression_for_l2(matrix_of_distance, pi_qwe_tree, plot_result=False):
    if type(pi_qwe_tree) == list:
        graph_position_vector_weight_vector = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list_tree,
                                                                                                    matrix_of_distance,
                                                                                                       norme=2)
        graph = graph_position_vector_weight_vector[0]
        position_vector = graph_position_vector_weight_vector[1]
        weight_vector = (graph_position_vector_weight_vector[2])

    else:

        graph = pi_qwe_tree
        position_vector = creat_position_vector_for_l2(graph)
        weight_vector = creat_weight_vector(graph)

    ir = IsotonicRegression( out_of_bounds = "clip")
    first_order = np.arange(len(position_vector))
    result_of_isotonic_regression = ir.fit_transform(first_order, taking_only_coordinates(position_vector),
                                                     sample_weight=taking_only_coordinates(weight_vector),
                                                    )

    # Make a list of tuple with NB of the vertices and the associate value the result

    list_tuple_with_nb_of_vertices_and_result_of_isotonic_regression = []
    for i in range(len(position_vector)):
        list_tuple_with_nb_of_vertices_and_result_of_isotonic_regression += \
            [(position_vector[i][0], result_of_isotonic_regression[i])]

    # #############################################################################

    # Plot result

    if plot_result:
        plt.figure()
        plt.plot(first_order, taking_only_coordinates(position_vector), 'r.', markersize=12)
        plt.plot(first_order, result_of_isotonic_regression, 'g.-', markersize=12)

        plt.legend(('Data', 'Isotonic Fit'), loc='lower right')
        plt.title('Isotonic regression')
        plt.show()

    return study_isotonic_regression_l2(matrix_of_distance, graph,
                                        list_tuple_with_nb_of_vertices_and_result_of_isotonic_regression)


distance = [[0, 1, 1, 1, 3],
            [1, 0, 1, 1, 3],
            [1, 1, 0, 1, 2],
            [1, 1, 1, 0, 3],
            [3, 3, 2, 3, 0]]

pi_qwe_list_tree = [P_NODE, [Q_NODE, [0], [P_NODE, [1], [2]], [3]], [4]]

print(make_isotonic_regression_for_l2(distance, pi_qwe_list_tree, plot_result=True))
