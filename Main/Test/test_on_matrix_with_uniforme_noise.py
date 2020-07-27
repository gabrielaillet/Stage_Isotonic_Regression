import unittest
from copy import deepcopy
from Main.Program.linear_programmation import change_format_of_pi_qwe_list, make_isotonic_for_l_1, \
    make_round_on_matrix, print_matrix, make_isotonic_for_l_inf, make_isotonic_regression_for_l2

from Main.Program.facade import facade_distance_between_matrices, facade_add_uniform_noise, \
    facade_standard_distance_from_pi_qew_tree, facade_from_pi_qew_tree_to_list, facade_random_generation_of_pi_qew_tree

class Test_Linear_Robinson_on_random_case_for_l_1(unittest.TestCase):

    def test_on_large_scale_for_l_1(self):
        for i in range(100):
            print("current iteration on large scale on l1 :", i)
            len_of_tree = 100
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 1)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[1]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[1]

            self.assertTrue(first_distance >= second_distance)

    def test_on_medium_scale_for_l_1(self):
        for i in range(250):
            print("current iteration on medium scale on l1 :", i)
            len_of_tree = 50
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 100)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[1]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[1]

            self.assertTrue(first_distance >= second_distance)

    def test_on_small_scale_for_l_1(self):
        for i in range(500):
            print("current iteration on small scale on l1 :", i)
            len_of_tree = 25
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 1)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[1]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[1]

            self.assertTrue(first_distance >= second_distance)

    def test_on_very_small_scale_for_l_1(self):
        for i in range(500):
            print("current iteration on very small scale on l1 :", i)
            len_of_tree = 10
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 10)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[1]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[1]
            self.assertTrue(first_distance >= second_distance)

    def test_on_one_example_for_l_1(self):
        len_of_tree = 5
        tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
        first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
        noise_matrix = deepcopy(first_matrix)
        tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
        tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
        facade_add_uniform_noise(noise_matrix, 1)
        isotonic_matrix = deepcopy(noise_matrix)
        make_isotonic_for_l_1(tree_to_use, isotonic_matrix, print_matrix_bool=False)
        make_round_on_matrix(isotonic_matrix)

        first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[1]
        second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[1]

        print('Tree on which the linear regression is apply', tree_to_use)
        print('The robinson matrix on which the test is made')
        print_matrix(first_matrix)
        print('The matrix that is now noisy')
        print_matrix(noise_matrix)
        print('The robinson matrix after the regression is made and rounded')
        print_matrix(isotonic_matrix)
        print('the distance between the initial matrix and the noisy one is',
              facade_distance_between_matrices(first_matrix, noise_matrix)[1])
        print('the distance between the initial matrix and the isotonic one is :',
              facade_distance_between_matrices(first_matrix, isotonic_matrix)[1])

        self.assertTrue(first_distance >= second_distance)


class Test_Linear_Robinson_on_random_case_for_l_inf(unittest.TestCase):

    def test_on_large_scale_for_l_inf(self):
        for i in range(100):
            print("current iteration on large scale on l_inf :", i)
            len_of_tree = 100
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 1)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[0]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[0]

            self.assertTrue(first_distance >= second_distance)

    def test_on_medium_scale_for_l_inf(self):
        for i in range(250):
            print("current iteration on medium scale on l_inf :", i)
            len_of_tree = 50
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 11)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[0]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[0]

            self.assertTrue(first_distance >= second_distance)

    def test_on_small_scale_for_l_inf(self):
        for i in range(250):
            print("current iteration on small scale on l_inf :", i)
            len_of_tree = 25
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 11)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[0]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[0]

            self.assertTrue(first_distance >= second_distance)

    def test_on_very_small_scale_for_l_inf(self):
        for i in range(500):
            print("current iteration on very small scale on l_inf :", i)
            len_of_tree = 10
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 5)
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[0]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[0]
            if first_distance < second_distance:
                print('Tree on which the linear regression is apply', tree_to_use)
                print('The robinson matrix on which the test is made')
                print_matrix(first_matrix)
                print('The matrix that is now noisy')
                print_matrix(noise_matrix)
                print('The robinson matrix after the regression is made and rounded')
                print_matrix(isotonic_matrix)
                print('the distance between the initial matrix and the noisy one is',
                      facade_distance_between_matrices(first_matrix, noise_matrix)[1])
                print('the distance between the initial matrix and the isotonic one is :',
                      facade_distance_between_matrices(first_matrix, isotonic_matrix)[1])
            self.assertTrue(first_distance >= second_distance)

    def test_on_one_example_for_l_1(self):
        len_of_tree = 10
        tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
        first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
        noise_matrix = deepcopy(first_matrix)
        tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
        tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
        facade_add_uniform_noise(noise_matrix, 11)
        isotonic_matrix = deepcopy(noise_matrix)
        make_isotonic_for_l_inf(tree_to_use, isotonic_matrix, print_matrix_bool=False)
        make_round_on_matrix(isotonic_matrix)

        first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[0]
        second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[0]

        print('Tree on which the linear regression is apply', tree_to_use)
        print('The robinson matrix on which the test is made')
        print_matrix(first_matrix)
        print('The matrix that is now noisy')
        print_matrix(noise_matrix)
        print('The robinson matrix after the regression is made and rounded')
        print_matrix(isotonic_matrix)
        print('the distance between the initial matrix and the noisy one is',
              facade_distance_between_matrices(first_matrix, noise_matrix)[1])
        print('the distance between the initial matrix and the isotonic one is :',
              facade_distance_between_matrices(first_matrix, isotonic_matrix)[1])

        self.assertTrue(first_distance >= second_distance)


class Test_Linear_Robinson_on_random_case_for_l_2(unittest.TestCase):

    def test_on_large_scale_for_l_2(self):
        for i in range(25):
            print("current iteration on large scale on l_2 :", i)
            len_of_tree = 50
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 10)
            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            while first_distance == 0:
                facade_add_uniform_noise(noise_matrix, 10)
                first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_regression_for_l2(tree_to_use, isotonic_matrix, print_matrix_bool=False)
            make_round_on_matrix(isotonic_matrix)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[2]
            print((first_distance - second_distance))
            self.assertTrue((first_distance - second_distance) >= -1)

    def test_on_medium_scale_for_l_2(self):
        for i in range(50):
            print("current iteration on medium scale on l_2 :", i)
            len_of_tree = 40
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 10)
            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            while first_distance == 0:
                facade_add_uniform_noise(noise_matrix, 1)
                first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_regression_for_l2(tree_to_use, isotonic_matrix, print_matrix_bool=False)

            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[2]

            self.assertTrue((first_distance - second_distance) >= -1)

    def test_on_small_scale_for_l_2(self):
        for i in range(100):
            print("current iteration on small scale on l_2 :", i)
            len_of_tree = 20
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 1)
            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
            while first_distance == 0:
                facade_add_uniform_noise(noise_matrix, 1)
                first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]

            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_regression_for_l2(tree_to_use, isotonic_matrix, print_matrix_bool=False)

            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[2]

            self.assertTrue((first_distance - second_distance) >= -1)

    def test_on_very_small_scale_for_l_2(self):
        for i in range(150):
            print("current iteration on very small scale on l_2 :", i)
            len_of_tree = 5
            tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
            first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
            noise_matrix = deepcopy(first_matrix)
            tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
            tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
            facade_add_uniform_noise(noise_matrix, 3)
            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]

            while first_distance == 0:
                facade_add_uniform_noise(noise_matrix, 1)
                first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]

            isotonic_matrix = deepcopy(noise_matrix)
            make_isotonic_regression_for_l2(tree_to_use, isotonic_matrix, print_matrix_bool=False)

            second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[2]

            self.assertTrue((first_distance - second_distance) >= -1)

    def test_on_one_example_for_l_2(self):
        len_of_tree = 10
        tree_to_use = facade_random_generation_of_pi_qew_tree(len_of_tree, 3)
        first_matrix = facade_standard_distance_from_pi_qew_tree(tree_to_use, len_of_tree)
        noise_matrix = deepcopy(first_matrix)
        tree_to_use = facade_from_pi_qew_tree_to_list(tree_to_use)
        tree_to_use = change_format_of_pi_qwe_list(tree_to_use)
        facade_add_uniform_noise(noise_matrix, 5)
        first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
        while first_distance == 0:
            facade_add_uniform_noise(noise_matrix, 1)
            first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
        isotonic_matrix = deepcopy(noise_matrix)
        make_isotonic_regression_for_l2(tree_to_use, isotonic_matrix, print_matrix_bool=False)
        make_round_on_matrix(isotonic_matrix)

        first_distance = facade_distance_between_matrices(first_matrix, noise_matrix)[2]
        second_distance = facade_distance_between_matrices(first_matrix, isotonic_matrix)[2]

        print('Tree on which the linear regression is apply', tree_to_use)
        print('The robinson matrix on which the test is made')
        print_matrix(first_matrix)
        print('The matrix that is now noisy')
        print_matrix(noise_matrix)
        print('The robinson matrix after the regression is made and rounded')
        print_matrix(isotonic_matrix)
        print('the distance between the initial matrix and the noisy one is :',
              facade_distance_between_matrices(first_matrix, noise_matrix)[2])
        print('the distance between the initial matrix and the isotonic one is :',
              facade_distance_between_matrices(first_matrix, isotonic_matrix)[2])

        self.assertTrue((first_distance - second_distance) >= -1)
