
from Main.Program.linear_programmation import change_format_of_pi_qwe_list, \
    make_round_on_matrix, make_isotonic_for_l_inf
import unittest
from Main.Program.facade import facade_distance_between_matrices, facade_geographic_distance
from copy import deepcopy


class Test_Linear_Robinson_on_random_case_for_l_inf(unittest.TestCase):

    def test_on_large_lenght(self):
        for i in range(100):
            matrix_with_distance = facade_geographic_distance(10, 5, 10, 50)
            list_changed_to_convention = change_format_of_pi_qwe_list(matrix_with_distance[1])
            first_matrix = deepcopy(matrix_with_distance[0])
            second_matrix = deepcopy(matrix_with_distance[0])
            make_isotonic_for_l_inf(list_changed_to_convention, second_matrix, print_matrix_bool=False)
            make_round_on_matrix(second_matrix)
            self.assertTrue(facade_distance_between_matrices(first_matrix, second_matrix)[0] <= 3)

    def test_on_large_height(self):
        for i in range(100):
            matrix_with_distance = facade_geographic_distance(10, 20, 2, 10)
            list_changed_to_convention = change_format_of_pi_qwe_list(matrix_with_distance[1])
            first_matrix = deepcopy(matrix_with_distance[0])
            second_matrix = deepcopy(matrix_with_distance[0])
            make_isotonic_for_l_inf(list_changed_to_convention, second_matrix, print_matrix_bool=False)
            make_round_on_matrix(second_matrix)
            self.assertTrue(facade_distance_between_matrices(first_matrix, second_matrix)[0] <= 10)
