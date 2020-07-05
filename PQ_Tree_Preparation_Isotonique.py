__author__ = 'Gabriel'

from Constant import *

def creat_position_vector_for_l1(pq_graph, position_vector=None):
    if position_vector is None:
        position_vector = []
    if pq_graph[TYPE] == LEAF:
        if (pq_graph[KEY], pq_graph[AVERAGE_DISTANCE][4]) in position_vector:
            return position_vector
        else:
            position_vector.append((pq_graph[KEY], 0))
            return position_vector
    else:
        if (pq_graph[LEAF], pq_graph[AVERAGE_DISTANCE][4]) not in position_vector:
            position_vector.append((pq_graph[KEY], pq_graph[AVERAGE_DISTANCE][4]))

        if pq_graph[TYPE] == P_NODE:
            for neighbors in pq_graph[NEIGHBORS]:
                creat_position_vector_for_l1(neighbors, position_vector)
        else:
            creat_position_vector_for_l1(pq_graph[NEIGHBORS][0], position_vector)
            creat_position_vector_for_l1(pq_graph[NEIGHBORS][1], position_vector)
        return position_vector


def creat_position_vector_for_l2(pq_graph, position_vector=None):
    if position_vector is None:
        position_vector = []
    mean = pq_graph[AVERAGE_DISTANCE][0] / pq_graph[AVERAGE_DISTANCE][1]
    if pq_graph[TYPE] == LEAF:
        if (pq_graph[KEY], mean) in position_vector:
            return position_vector
        else:
            position_vector.append((pq_graph[KEY], 0))
            return position_vector
    else:
        if (pq_graph[KEY], mean) not in position_vector:
            position_vector.append((pq_graph[KEY], mean))
        if pq_graph[TYPE] == P_NODE:
            for neighbors in pq_graph[NEIGHBORS]:
                creat_position_vector_for_l1(neighbors, position_vector)
        else:
            creat_position_vector_for_l2(pq_graph[NEIGHBORS][0], position_vector)
            creat_position_vector_for_l2(pq_graph[NEIGHBORS][1], position_vector)
        return position_vector


def creat_position_vector_for_l_inf(pq_graph, position_vector=None):
    if position_vector is None:
        position_vector = []
    min_max = (pq_graph[AVERAGE_DISTANCE][2] + pq_graph[AVERAGE_DISTANCE][3]) / 2
    if pq_graph[TYPE] == LEAF:
        if (pq_graph[KEY], min_max) in position_vector:
            return position_vector
        else:
            position_vector.append((pq_graph[KEY], 0))
            return position_vector
    else:
        if (pq_graph[KEY], min_max) not in position_vector:
            position_vector.append((pq_graph[KEY], min_max))

        if pq_graph[TYPE] == P_NODE:
            for neighbors in pq_graph[NEIGHBORS]:
                creat_position_vector_for_l1(neighbors, position_vector)
        else:
            creat_position_vector_for_l_inf(pq_graph[NEIGHBORS][0], position_vector)
            creat_position_vector_for_l_inf(pq_graph[NEIGHBORS][1], position_vector)
        return position_vector


def creat_weight_vector(pq_graph, weight_vector=None):
    if weight_vector is None:
        weight_vector = []
    if pq_graph[TYPE] == LEAF:
        if (pq_graph[KEY], 1) not in weight_vector:
            weight_vector.append((pq_graph[KEY], pq_graph[AVERAGE_DISTANCE][1]))
            return weight_vector
    else:
        weight_vector.append((pq_graph[KEY], pq_graph[AVERAGE_DISTANCE][1]))
        if pq_graph[TYPE] == P_NODE:
            for neighbors in pq_graph[NEIGHBORS]:
                creat_position_vector_for_l1(neighbors, weight_vector)
        else:
            creat_position_vector_for_l2(pq_graph[NEIGHBORS][0], weight_vector)
            creat_position_vector_for_l2(pq_graph[NEIGHBORS][1], weight_vector)
        return weight_vector
