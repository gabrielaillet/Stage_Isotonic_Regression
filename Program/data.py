__author__ = 'Gabriel'
from Program.Constant import *
from Program.PQ_Tree_To_Graph_Transformation import from_pi_qew_tree_to_basic_graph_with_position_and_weight

class Data():
    def __init__(self,distance,pi_qwe_list,norme):
        graph, self.position_vector, self.weight_vector = from_pi_qew_tree_to_basic_graph_with_position_and_weight\
            (pi_qwe_list, distance, norme)
        self.graph = Graph(graph)


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








