__author__ = 'Gabriel'

from Main.foreign_program.Constant import *


def study_isotonic_regression_l2(distance, graph, exploited_points):
    robinson_dissimilarity = distance
    current_graph = graph
    value_to_change = find_value_in_vector(current_graph[KEY], exploited_points)

    if current_graph[TYPE] == LEAF:
        return distance
    if current_graph[TYPE] == Q_NODE:
        represent1 = current_graph[REPRESENTS][0][POINTS]
        represent2 = current_graph[REPRESENTS][1][POINTS]
        for n1 in represent1:
            for n2 in represent2:
                if n1 != n2:
                    robinson_dissimilarity[n1][n2] = value_to_change
                    robinson_dissimilarity[n2][n1] = value_to_change
            robinson_dissimilarity = study_isotonic_regression_l2(robinson_dissimilarity, current_graph[NEIGHBORS][0],
                                                                  exploited_points)
            robinson_dissimilarity = study_isotonic_regression_l2(robinson_dissimilarity, current_graph[NEIGHBORS][1],
                                                                  exploited_points)

    if current_graph[TYPE] == P_NODE:
        for points1 in current_graph[POINTS]:
            for points2 in current_graph[POINTS]:
                if points1 != points2:
                    robinson_dissimilarity[points1][points2] = value_to_change
                    robinson_dissimilarity[points2][points1] = value_to_change

        for neighbors in current_graph[NEIGHBORS]:
            robinson_dissimilarity = study_isotonic_regression_l2(robinson_dissimilarity, neighbors,
                                                                  exploited_points)

    return robinson_dissimilarity


def find_value_in_vector(value_to_find, vector):
    for coordinates in vector:
        if coordinates[0] == value_to_find:
            return coordinates[1]
    return None
