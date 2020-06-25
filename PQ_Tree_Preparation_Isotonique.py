__author__ = 'Gabriel'
from PQ_Tree_To_Graph_Transformation import *



def creat_position_vector_for_L1(PQ_graph, Position_vector = []):
    if (PQ_graph[TYPE] == LEAF):
        if (PQ_graph[KEY],PQ_graph[AVERAGE_DISTANCE][4]) in Position_vector:
            return Position_vector
        else:
            Position_vector.append((PQ_graph[KEY], 0))
            return Position_vector
    else:
        if (PQ_graph[LEAF],PQ_graph[AVERAGE_DISTANCE][4]) not in Position_vector:
            Position_vector.append((PQ_graph[KEY], PQ_graph[AVERAGE_DISTANCE][4]))
        creat_position_vector_for_L1(PQ_graph[NEIGHBORS][0], Position_vector)
        creat_position_vector_for_L1(PQ_graph[NEIGHBORS][1], Position_vector)
        return Position_vector


def creat_position_vector_for_L2(PQ_graph, Postion_vector = []):
    mean = PQ_graph[AVERAGE_DISTANCE][0]/PQ_graph[AVERAGE_DISTANCE][1]
    if (PQ_graph[TYPE] == LEAF):
        if (PQ_graph[KEY],mean) in Postion_vector:
            return Postion_vector
        else:
            Postion_vector.append((PQ_graph[KEY], 0))
            return Postion_vector
    else:
        if (PQ_graph[KEY],mean) not in Postion_vector:
            Postion_vector.append((PQ_graph[KEY], mean))
        creat_position_vector_for_L2(PQ_graph[NEIGHBORS][0], Postion_vector)
        creat_position_vector_for_L2(PQ_graph[NEIGHBORS][1], Postion_vector)
        return Postion_vector

def creat_position_vector_for_L_inf(PQ_graph, Position_vector = []):
    min_max = (PQ_graph[AVERAGE_DISTANCE][2]+PQ_graph[AVERAGE_DISTANCE][3])/2
    if (PQ_graph[TYPE] == LEAF):
        if (PQ_graph[KEY],min_max) in Position_vector:
            return Position_vector
        else:
            Position_vector.append((PQ_graph[KEY], 0))
            return Position_vector
    else:
        if (PQ_graph[KEY],min_max) not in Position_vector:
            Position_vector.append((PQ_graph[KEY], min_max))
        creat_position_vector_for_L_inf(PQ_graph[NEIGHBORS][0], Position_vector)
        creat_position_vector_for_L_inf(PQ_graph[NEIGHBORS][1], Position_vector)
        return Position_vector

def creat_weight_vector(PQ_graph, Weight_vector = []):
    if (PQ_graph[TYPE] == LEAF):
        if (PQ_graph[KEY], 1) not in Weight_vector:
            Weight_vector.append((PQ_graph[KEY], PQ_graph[AVERAGE_DISTANCE][1]))
            return Weight_vector
    else:
        Weight_vector.append((PQ_graph[KEY], PQ_graph[AVERAGE_DISTANCE][1]))
        creat_weight_vector(PQ_graph[NEIGHBORS][0], Weight_vector)
        creat_weight_vector(PQ_graph[NEIGHBORS][1], Weight_vector)
        return Weight_vector
