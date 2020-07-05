__author__ = 'Gabriel'
from Constant import *
from PQ_Tree_To_Graph_Transformation import from_pi_qew_tree_to_basic_graph_with_position_and_weight

class facade():
    def __init__(self,distance,pi_qwe_list,norme):
        self.graph,self.vector_pos,self.vector_weight = from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qwe_list,distance,norme)


class Graph():
    def __init__(self,graph_to_transform):

        self.type = graph_to_transform[TYPE]
        self.key = graph_to_transform[KEY]
        self.points = graph_to_transform[POINTS]
        self.average_distance = graph_to_transform[AVERAGE_DISTANCE]

        if graph_to_transform[TYPE] == LEAF:
            self.neighbors = graph_to_transform[NEIGHBORS]


        elif graph_to_transform[TYPE] == Q_NODE:
            self.neighbors = []
            self.represents = []
            for represents in graph_to_transform[REPRESENTS]:
                self.represents += [Graph(represents)]
            for neighbors in graph_to_transform[NEIGHBORS]:
                self.neighbors += [Graph(neighbors)]
        else:
            self.neighbors = []
            for neighbors in graph_to_transform[NEIGHBORS]:
                self.neighbors += [Graph(neighbors)]








distance = [[0, 1, 1, 4, 3],
            [1 , 0, 1, 4, 3],
            [1, 1, 0, 4, 3],
            [4, 4, 4, 0, 3],
            [3,3, 3, 3, 0]]

pi_qwe_list_tree = [Q_NODE, [P_NODE, [0],[1],[2]], [3], [4]]

a = facade(distance,pi_qwe_list_tree,1)
print(a.graph.neighbors[0].key)
