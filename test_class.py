import unittest

from PQ_Tree_To_Graph_Transformation import from_pi_qew_tree_to_basic_graph_with_position_and_weight, \
    from_pi_qew_tree_to_basic_graph, taking_only_coordinates
from facade import Graph
from Constant import *


class Test_Q_Tree_To_Graph_Trivial(unittest.TestCase):

    def setUp(self) -> None:
        self.distanceTwo = [[0, 2, 2, 2, 2],
                            [2, 0, 2, 2, 2],
                            [2, 2, 0, 2, 2],
                            [2, 2, 2, 0, 2],
                            [2, 2, 2, 2, 0]]

        self.Q_list = [Q_NODE, [0], [1], [2]]

    def testQ_graph(self):
        list_to_use = self.Q_list
        distance = self.distanceTwo
        q_graph = from_pi_qew_tree_to_basic_graph(list_to_use, distance)
        type_expected = Q_NODE
        points_represent_expected_on_root_first = [0]
        points_represent_expected_on_root_second = [2]
        points_represent_expected_on_first_neighbors_first = [0]
        points_represent_expected_on_first_neighbors_second = [1]
        points_represent_expected_on_second_neighbors_first = [1]
        points_represent_expected_on_second_neighbors_second = [2]

        self.assertTrue(
            q_graph[TYPE] == type_expected)
        self.assertTrue(
            q_graph[REPRESENTS][0][POINTS] == points_represent_expected_on_root_first)
        self.assertTrue(
            q_graph[REPRESENTS][1][POINTS] == points_represent_expected_on_root_second)
        self.assertTrue(
            q_graph[NEIGHBORS][0][REPRESENTS][0][POINTS] == points_represent_expected_on_first_neighbors_first)
        self.assertTrue(
            q_graph[NEIGHBORS][0][REPRESENTS][1][POINTS] == points_represent_expected_on_first_neighbors_second)
        self.assertTrue(
            q_graph[NEIGHBORS][1][REPRESENTS][0][POINTS] == points_represent_expected_on_second_neighbors_first)
        self.assertTrue(
            q_graph[NEIGHBORS][1][REPRESENTS][1][POINTS] == points_represent_expected_on_second_neighbors_second)


class Test_P_Tree_To_Graph_Trivial(unittest.TestCase):
    def setUp(self) -> None:
        self.distanceTwo = [[0, 2, 2, 2, 2],
                            [2, 0, 2, 2, 2],
                            [2, 2, 0, 2, 2],
                            [2, 2, 2, 0, 2],
                            [2, 2, 2, 2, 0]]

        self.P_list = [P_NODE, [0], [1], [2]]

    def testP_graph(self):
        list_to_use = self.P_list
        distance = self.distanceTwo
        p_graph = from_pi_qew_tree_to_basic_graph(list_to_use, distance)
        type_expected = P_NODE
        point_expected = [0, 1, 2]
        self.assertTrue(p_graph[TYPE] == type_expected and p_graph[POINTS] == point_expected)


class Test_Distance_Vector_on_trivial_example(unittest.TestCase):
    def setUp(self) -> None:
        self.distanceTwo = [[0, 2, 2, 2, 2],
                            [2, 0, 2, 2, 2],
                            [2, 2, 0, 2, 2],
                            [2, 2, 2, 0, 2],
                            [2, 2, 2, 2, 0]]

        self.pi_qwe_list = [Q_NODE, [P_NODE, [0], [1], [4]], [2], [3]]

    def test_position_Vectors_is_true_L1_distanceTwo(self):
        pi_qwe_list = self.pi_qwe_list
        distance = self.distanceTwo
        expected = [2, 2, 2, 2]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list, distance)[1]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_vectors_is_true_l2_distance_two(self):
        pi_qwe_list = self.pi_qwe_list
        distance = self.distanceTwo
        expected = [2, 2, 2, 2]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list, distance, norme=2)[1]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_vectors_is_true_l_inf_distance_two(self):
        complex_list = self.pi_qwe_list
        distance = self.distanceTwo
        expected = [2, 2, 2, 2]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(complex_list, distance, norme='inf')[1]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)


class Test_Distance_Vector_on_a_more_complex_distance(unittest.TestCase):
    def setUp(self) -> None:
        self.distance = [[0, 1, 2, 3, 3],
                         [1, 0, 2, 3, 2],
                         [2, 2, 0, 3, 2],
                         [3, 3, 3, 0, 9],
                         [2, 2, 2, 9, 0]]

        self.pi_qwe_list = [Q_NODE, [P_NODE, [0], [1], [4]], [2], [3]]

    def test_position_Vectors_is_true_L1(self):
        complex_list = self.pi_qwe_list
        distance = self.distance
        expected = [2, 2, 3, 3]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(complex_list, distance)[1]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_Vectors_is_true_L2(self):
        complex_list = self.pi_qwe_list
        distance = self.distance
        expected = [2, 2, 3, 5]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(complex_list, distance, norme=2)[1]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_Vectors_is_true_L_inf_distanceComplex(self):
        complex_list = self.pi_qwe_list
        distance = self.distance
        expected = [2, 2, 3, 6]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(complex_list, distance, norme='inf')[1]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)


class Test_Weight_Vector(unittest.TestCase):
    def setUp(self) -> None:
        self.distance = [[0, 1, 2, 3, 3],
                         [1, 0, 2, 3, 2],
                         [2, 2, 0, 3, 2],
                         [3, 3, 3, 0, 9],
                         [2, 2, 2, 9, 0]]

        self.pi_qwe_list = [Q_NODE, [P_NODE, [0], [1], [4]], [2], [3]]

    def test_weight_Vectors_are_the_same_and_are_true(self):
        complex_list = self.pi_qwe_list
        distance = self.distance
        expected = [3, 3, 1, 3]

        value = from_pi_qew_tree_to_basic_graph_with_position_and_weight(complex_list, distance)[2]
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)
