import unittest
from Main.Program.linear_programmation import change_format_of_pi_qwe_list, make_isotonic_for_l_1, make_round_on_matrix, \
    print_matrix, make_isotonic_for_l_inf
from Main.foreign_program.Diverse_Functions import distance_between_matrices
from Main.foreign_program.Matrix_Construction_and_Modification import standard_distance_from_pi_qew_tree, \
    add_non_uniform_noise
from copy import deepcopy
from Main.foreign_program.type_conversions_for_PQ_trees import from_pi_qew_tree_to_list
from Main.foreign_program.Global_Functions_for_PQ_Trees import random_generation_of_pi_qew_tree
from random import randint


class Test_Linear_Robinson_on_random_case_for_l_1(unittest.TestCase):

    def test_on_large_scale_for_l_1(self):
        for i in range(500):
            len_of_tree = randint(2, 25)
            tree_to_use = random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            add_non_uniform_noise(noise_matrix, 10, 1)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = distance_between_matrices(first_matrix, noise_matrix)[1]
            second_distance = distance_between_matrices(first_matrix, isotonic_matrix)[1]

            self.assertTrue(first_distance >= second_distance)

    def test_on_small_scale_for_l_1(self):
        len_of_tree = randint(2, 25)
        tree_to_use = random_generation_of_pi_qew_tree(len_of_tree, 3)
        first_matrix = standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
        noise_matrix = deepcopy(first_matrix)
        tree_to_use = from_pi_qew_tree_to_list(tree_to_use)
        tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
        add_non_uniform_noise(noise_matrix, 10, 1)
        isotonic_matrix = deepcopy(noise_matrix)
        make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix=False)
        make_round_on_matrix(isotonic_matrix)

        first_distance = distance_between_matrices(first_matrix, noise_matrix)[1]
        second_distance = distance_between_matrices(first_matrix, isotonic_matrix)[1]

        print('Tree on which the linear regression is apply', tree_to_use)
        print('The robinson matrix on which the test is made')
        print_matrix(first_matrix)
        print('The matrix that is now noisy')
        print_matrix(noise_matrix)
        print('The robinson matrix after the regression is made and rounded')
        print_matrix(isotonic_matrix)
        print('la distance entre la matrice initiale et la matrice bruite est',
              distance_between_matrices(first_matrix, noise_matrix)[1])
        print('la distance entre la matrice initiale et la matrice iso est',
              distance_between_matrices(first_matrix, isotonic_matrix)[1])

        self.assertTrue(first_distance >= second_distance)


class Test_Linear_Robinsson_on_random_case_for_l_inf(unittest.TestCase):

    def test_on_large_scale_for_l_inf(self):
        for i in range(500):
            len_of_tree = randint(2, 25)
            tree_to_use = random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            add_non_uniform_noise(noise_matrix, 10, 1)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = distance_between_matrices(first_matrix, noise_matrix)[0]
            second_distance = distance_between_matrices(first_matrix, isotonic_matrix)[0]

            self.assertTrue(first_distance >= second_distance)

    def test_on_small_scale_for_l_inf(self):
        len_of_tree = 6
        tree_to_use = random_generation_of_pi_qew_tree(len_of_tree, 3)
        first_matrix = standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
        noise_matrix = deepcopy(first_matrix)
        tree_to_use = from_pi_qew_tree_to_list(tree_to_use)
        tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
        add_non_uniform_noise(noise_matrix, 10, 1)
        isotonic_matrix = deepcopy(noise_matrix)
        make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix=False)
        make_round_on_matrix(isotonic_matrix)

        first_distance = distance_between_matrices(first_matrix, noise_matrix)[0]
        second_distance = distance_between_matrices(first_matrix, isotonic_matrix)[0]

        print('Tree on which the linear regression is apply', tree_to_use)
        print('The robinson matrix on which the test is made')
        print_matrix(first_matrix)
        print('The matrix that is now noisy')
        print_matrix(noise_matrix)
        print('The robinson matrix after the regression is made and rounded')
        print_matrix(isotonic_matrix)
        print('la distance entre la matrice initiale et la matrice bruite est',
              distance_between_matrices(first_matrix, noise_matrix)[1])
        print('la distance entre la matrice initiale et la matrice iso est',
              distance_between_matrices(first_matrix, isotonic_matrix)[1])

        self.assertTrue(first_distance >= second_distance)
