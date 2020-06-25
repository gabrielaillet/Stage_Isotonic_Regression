__author__ = 'Gabriel'
import matplotlib.pyplot as plt
import numpy as np
from sklearn.isotonic import IsotonicRegression

from Explotation_Isotonique_Regression import *
from PQ_Tree_Preparation_Isotonique import *

distance = [[0, 5, 4, 3, 10],
            [5, 0, 1, 2, 8],
            [4, 1, 0, 1, 9],
            [3, 2, 1, 0, 7],
            [10, 8, 9, 7, 0]]

pi_qwe_list_tree = [Q_NODE, [4], [P_NODE, [3], [1], [2]], [0]]
graph_position_vector_weight_vector = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list_tree,
                                                                                               distance, norme=2)
graph = graph_position_vector_weight_vector[0]

position_vector = taking_only_coordinates(graph_position_vector_weight_vector[1])
weight_vector = taking_only_coordinates((graph_position_vector_weight_vector[2]))

# #############################################################################
# Fit IsotonicRegression and LinearRegression models

ir = IsotonicRegression()
first_order = np.arange(len(position_vector))
result_of_isotonic_regression = ir.fit_transform(first_order, position_vector, sample_weight=weight_vector)

# Make a list of tuple with NB of the vertices and the associate value the result

list_tuple_with_nb_of_vertices_and_result_of_isotonic_regression = []
for i in range(len(graph_position_vector_weight_vector[1])):
    list_tuple_with_nb_of_vertices_and_result_of_isotonic_regression += \
        [(graph_position_vector_weight_vector[1][i][0], result_of_isotonic_regression[i])]

# #############################################################################
print(study_isotonic_regression_l2(distance, graph_position_vector_weight_vector[0],
                                   list_tuple_with_nb_of_vertices_and_result_of_isotonic_regression))

# Plot result


fig = plt.figure()
plt.plot(first_order, position_vector, 'r.', markersize=12)
plt.plot(first_order, result_of_isotonic_regression, 'g.-', markersize=12)

plt.legend(('Data', 'Isotonic Fit'), loc='lower right')
plt.title('Isotonic regression')
plt.show()



