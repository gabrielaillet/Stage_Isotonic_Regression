import unittest

from Main.foreign_program.PQ_Tree_To_Graph_Transformation import taking_only_coordinates
from Main.Program.data import Data


class Test_Q_Tree_To_Graph_Trivial(unittest.TestCase):

    def setUp(self) -> None:
        self.distanceTwo = [[0, 2, 2, 2, 2],
                            [2, 0, 2, 2, 2],
                            [2, 2, 0, 2, 2],
                            [2, 2, 2, 0, 2],
                            [2, 2, 2, 2, 0]]

        self.Q_list = ['Q_node', [0], [1], [2]]

    def testQ_graph(self):
        list_to_use = self.Q_list
        distance = self.distanceTwo
        q_graph = Data(distance, list_to_use, 1).graph
        type_expected = 'Q_node'
        points_represent_expected_on_root_first = [0]
        points_represent_expected_on_root_second = [2]
        points_represent_expected_on_first_neighbors_first = [0]
        points_represent_expected_on_first_neighbors_second = [1]
        points_represent_expected_on_second_neighbors_first = [1]
        points_represent_expected_on_second_neighbors_second = [2]

        self.assertTrue(
            q_graph.type == type_expected)
        self.assertTrue(
            q_graph.represents[0].points == points_represent_expected_on_root_first)
        self.assertTrue(
            q_graph.represents[1].points == points_represent_expected_on_root_second)
        self.assertTrue(
            q_graph.neighbors[0].represents[0].points == points_represent_expected_on_first_neighbors_first)
        self.assertTrue(
            q_graph.neighbors[0].represents[1].points == points_represent_expected_on_first_neighbors_second)
        self.assertTrue(
            q_graph.neighbors[1].represents[0].points == points_represent_expected_on_second_neighbors_first)
        self.assertTrue(
            q_graph.neighbors[1].represents[1].points == points_represent_expected_on_second_neighbors_second)


class Test_P_Tree_To_Graph_Trivial(unittest.TestCase):
    def setUp(self) -> None:
        self.distanceTwo = [[0, 2, 2, 2, 2],
                            [2, 0, 2, 2, 2],
                            [2, 2, 0, 2, 2],
                            [2, 2, 2, 0, 2],
                            [2, 2, 2, 2, 0]]

        self.P_list = ['P_node', [0], [1], [2]]

    def testP_graph(self):
        list_to_use = self.P_list
        distance = self.distanceTwo
        p_graph = Data(distance, list_to_use, 1).graph
        type_expected = 'P_node'
        point_expected = [0, 1, 2]
        self.assertTrue(p_graph.type == type_expected and p_graph.points == point_expected)


class Test_Distance_Vector_on_trivial_example(unittest.TestCase):
    def setUp(self) -> None:
        self.distanceTwo = [[0, 2, 2, 2, 2],
                            [2, 0, 2, 2, 2],
                            [2, 2, 0, 2, 2],
                            [2, 2, 2, 0, 2],
                            [2, 2, 2, 2, 0]]

        self.pi_qwe_list = ['Q_node', ['P_node', [0], [1], [4]], [2], [3]]

    def test_position_Vectors_is_true_L1_distanceTwo(self):
        pi_qwe_list = self.pi_qwe_list
        distance = self.distanceTwo
        expected = [0, 0, 0, 2, 0, 0, 2, 2, 2]

        value = Data(distance, pi_qwe_list, 1).position_vector
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_vectors_is_true_l2_distance_two(self):
        pi_qwe_list = self.pi_qwe_list
        distance = self.distanceTwo
        expected = [0, 0, 0, 2, 0, 0, 2, 2, 2]

        value = Data(distance, pi_qwe_list, 2).position_vector
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_vectors_is_true_l_inf_distance_two(self):
        pi_qwe_list = self.pi_qwe_list
        distance = self.distanceTwo
        expected = [0, 0, 0, 2, 0, 0, 2, 2, 2]

        value = Data(distance, pi_qwe_list, 'inf').position_vector
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)


class Test_Distance_Vector_on_a_more_complex_distance(unittest.TestCase):
    def setUp(self) -> None:
        self.distance = [[0, 1, 2, 3, 3],
                         [1, 0, 2, 3, 2],
                         [2, 2, 0, 3, 2],
                         [3, 3, 3, 0, 9],
                         [2, 2, 2, 9, 0]]

        self.pi_qwe_list = ['Q_node', ['P_node', [0], [1], [4]], [2], [3]]

    def test_position_Vectors_is_true_L1(self):
        the_more_complex_pi_qwe_list = self.pi_qwe_list
        distance = self.distance
        expected = [0, 0, 0, 2, 0, 0, 2, 3, 3]

        value = Data(distance, the_more_complex_pi_qwe_list, 1).position_vector
        value = taking_only_coordinates(value)
        self.assertTrue(value == expected)

    def test_position_Vectors_is_true_L2(self):
        the_more_complex_pi_qwe_list = self.pi_qwe_list
        distance = self.distance
        expected = [0, 0, 0, 2, 0, 0, 2, 3, 5]

        value = Data(distance, the_more_complex_pi_qwe_list, 2).position_vector
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)

    def test_position_Vectors_is_true_L_inf_distanceComplex(self):
        the_more_complex_pi_qwe_list = self.pi_qwe_list
        distance = self.distance
        expected = [0, 0, 0, 2, 0, 0, 2, 3, 6]

        value = Data(distance, the_more_complex_pi_qwe_list, 'inf').position_vector
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)


class Test_Weight_Vector(unittest.TestCase):
    def setUp(self) -> None:
        self.distance = [[0, 1, 2, 3, 3],
                         [1, 0, 2, 3, 2],
                         [2, 2, 0, 3, 2],
                         [3, 3, 3, 0, 9],
                         [2, 2, 2, 9, 0]]

        self.pi_qwe_list = ['Q_node', ['P_node', [0], [1], [4]], [2], [3]]

    def test_weight_Vectors_is_true(self):
        complex_list = self.pi_qwe_list
        distance = self.distance
        expected = [1, 1, 1, 3, 1, 1, 3, 1, 3]

        value = Data(distance, complex_list, 1).weight_vector
        value = taking_only_coordinates(value)

        self.assertTrue(value == expected)
