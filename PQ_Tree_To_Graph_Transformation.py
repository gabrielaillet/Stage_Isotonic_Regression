__author__ = 'pascal'

from statistics import median

"""
The aim of this module is, given a dissimilarity "distance", to provide tools to transform a given PQ-tree
    (given as a 'PQ-list' "pi_qew_list") into a graph on which ISOTONIC REGRESSION will give the best Robinson
    approximation of "distance" among the Robinson dissimilarities admitting "pi_qew_list" as PQ-tree.
Contains the functions :


    "from_pi_qew_tree_to_basic_graph"
        which, given a PQ-tree "pi_qew_list" and a dissimilarity "distance",
        returns an acyclic digraph on which the ISOTONIC REGRESSION gives the Robinson dissimilarity
        admitting "pi_qew_list" as PQ-tree which is the closest to "distance".
        - INPUT:
            The PQ-tree is given as a list
                e.g. ['P_node', ['Q_node', 9, 3, 1], ['P_node', 0, 6, 7, ['P_node', 8, 5, ['P_node', 4, 2]]]]
            The dissimilarity as a matrix, i.e. a list of list.
        - OUTPUT:
        Each node x of the result (the digraph) is given as a dictionary whose keys (and elements) are:
            KEY ("key) is a number (settled by global variable NB in the code), different for each node.
            NEIGHBORS ("neighbors") are the neighbors of x (nodes y such that x --> y is an arc), given as a list
            POINTS ("points") is the list of the leaves (of the PQ-tree) under x (for internal use only)
            AVERAGE_DISTANCE ("average_dist") calculated by the function "average_distance",
                is a quintuple (dist_sum, dist_nb, dist_max, dist_min, median) where
                    - dist_sum is the sum of the distances involved by node x
                    - dist_nb is the number of the distances involved by x.
                    - dist_max is the greatest distance involved by x
                    - dist_min is the smalest distince involved by x
                    - median is the median value of all calculated distance involved by x
                For a isotonic regression program, dist_sum / dist_nb (or dist_max in L_inf norm) would be
                the value associated with x, and dist_nb the weight of node x.
            TYPE ("type") indicates if the node (of the graph) comes from a P_node, a Q-node or a Leaf
            REPRESENTS ("represents") indicates, for a vertex x coming from a Q-node, the two (tree) nodes whose
                distance is represented by x. this will be used to construct the approximate Robinson distance.
        - REMARKS :
            - If x --> y is an arc of the digraph, then the values val(x) and val(y) after the ISOTONIC REGRESSION
                should verify val(x) >= val(y).
            - Actually, the result is the dictionary corresponding with the node which is the (unique) source
                of the acyclic digraph
            - No verification is made on the distance. Be careful that:
                - it is square and symmetric with 0 on the diagonal
                - it has the same "size" that the PQ-tree (if the matrix is smaller, the program fail)
        - This function uses the functions (from this module):
            - from_pi_node_to_basic_graph
            - from_qew_node_to_basic_graph
            - average_distance
        and ALL Global variables


    "from_basic_graph_to_adjacency_list"
        which, given a graph "basic_graph", built by function from_pi_qew_tree_to_basic_graph, constructs an
        adjacency list which represents the same graph.
        The result ("adjacency_list") is given as a list of n+1 elements, where n is the number of vertices
        - REMARKS:
            - The vertices are numbered from 1 to n
            - The first element ("adjacency_list[0]") is not used
            - Each element of "adjacency_list" is a dictionary with two keys :
                - AVERAGE_DISTANCE ("average_dist") is the same as in "basic_graph"
                - NEIGHBORS ("neighbors") is the list of the neighbors of the vertex
            - In order to construct the approximate Robinson dissimilarity, "basic_graph" is NECESSARY.
        - This function uses the function (from this module):
            - recursive_from_basic_graph_to_adjacency_list
        and Global variables
            - "AVERAGE_DISTANCE"
            - "NEIGHBORS"
            - "KEY"
            
            
    "from_pi_qew_tree_to_basic_graph_with_position"
         which, given a PQ-tree "pi_qew_list" and a dissimilarity "distance",
        returns an acyclic digraph on which the ISOTONIC REGRESSION gives the Robinson dissimilarity
        admitting "pi_qew_list" as PQ-tree which is the closest to "distance" with the position vector necessary to 
        make an isotonic regression.
        - INPUT:
            The PQ-tree is given as a list
                e.g. ['Q_node', ['P_node', [0], [1]], [2], [3]]
            The dissimilarity as a matrix, i.e. a list of list.
            The norm witch we want to make the isotonic regression by default norm = 1 (can take 3 value {1,2,'inf'})
            
         - OUTPUT:
        -Each node x of the result (the digraph) is given as a dictionary whose keys (and elements) are:
            KEY ("key) is a number (settled by global variable NB in the code), different for each node.
            NEIGHBORS ("neighbors") are the neighbors of x (nodes y such that x --> y is an arc), given as a list
            POINTS ("points") is the list of the leaves (of the PQ-tree) under x (for internal use only)
            AVERAGE_DISTANCE ("average_dist") calculated by the function "average_distance",
                is a quintuple (dist_sum, dist_nb, dist_max) where
                    - dist_sum is the sum of the distances involved by node x
                    - dist_nb is the number of the distances involved by x.
                    - dist_max is the greatest distance involved by x
                    - dist_min is the smalest distince involved by x
                    - median is the median value of all calculated distance involved by x
                For a isotonic regression program, dist_sum / dist_nb (or dist_max in L_inf norm) would be
                the value associated with x, and dist_nb the weight of node x.
            TYPE ("type") indicates if the node (of the graph) comes from a P_node, a Q-node or a Leaf
            REPRESENTS ("represents") indicates, for a vertex x coming from a Q-node, the two (tree) nodes whose
                distance is represented by x. this will be used to construct the approximate Robinson distance.
        -position is a list of tuple with the Key of vertices and the actual position of that vertices
        - This function uses the functions (from this module):
            - from_pi_node_to_basic_graph_with_position
            - from_qew_node_to_basic_graph_with_position
            - average_distance
        and ALL Global variables
        
        "from_pi_qew_tree_to_basic_graph_with_weight"
         which, given a PQ-tree "pi_qew_list" and a dissimilarity "distance",
        returns an acyclic digraph on which the ISOTONIC REGRESSION gives the Robinson dissimilarity
        admitting "pi_qew_list" as PQ-tree which is the closest to "distance" with the position vector necessary to 
        make an isotonic regression.
        - INPUT:
            The PQ-tree is given as a list
                e.g. ['Q_node', ['P_node', [0], [1]], [2], [3]]
            The dissimilarity as a matrix, i.e. a list of list.
            The norm witch we want to make the isotonic regression by default norm = 1 (can take 3 value {1,2,'inf'})
            
         - OUTPUT:
        -Each node x of the result (the digraph) is given as a dictionary whose keys (and elements) are:
            KEY ("key) is a number (settled by global variable NB in the code), different for each node.
            NEIGHBORS ("neighbors") are the neighbors of x (nodes y such that x --> y is an arc), given as a list
            POINTS ("points") is the list of the leaves (of the PQ-tree) under x (for internal use only)
            AVERAGE_DISTANCE ("average_dist") calculated by the function "average_distance",
                is a quintuple (dist_sum, dist_nb, dist_max) where
                    - dist_sum is the sum of the distances involved by node x
                    - dist_nb is the number of the distances involved by x.
                    - dist_max is the greatest distance involved by x
                    - dist_min is the smalest distince involved by x
                    - median is the median value of all calculated distance involved by x
                For a isotonic regression program, dist_sum / dist_nb (or dist_max in L_inf norm) would be
                the value associated with x, and dist_nb the weight of node x.
            TYPE ("type") indicates if the node (of the graph) comes from a P_node, a Q-node or a Leaf
            REPRESENTS ("represents") indicates, for a vertex x coming from a Q-node, the two (tree) nodes whose
                distance is represented by x. this will be used to construct the approximate Robinson distance.
        -weight is a list of tuple with the Key of vertices and the actual weight of that vertices
        - This function uses the functions (from this module):
            - from_pi_node_to_basic_graph_with_weight
            - from_qew_node_to_basic_graph_with_weight
            - average_distance
        and ALL Global variables
"""

P_NODE = 'P_node'
Q_NODE = 'Q_node'
LEAF = 'leaf'
AVERAGE_DISTANCE = "average_dist"
NEIGHBORS = "neighbors"
POINTS = "points"
KEY = "key"
TYPE = "type"
REPRESENTS = "represents"
NB = 0

""" ####################################################################################### """


def from_pi_qew_tree_to_basic_graph(pi_qew_list, distance):
    global NB

    if pi_qew_list[0] == P_NODE:
        return from_pi_node_to_basic_graph(pi_qew_list, distance)
    if pi_qew_list[0] == Q_NODE:
        return from_qew_node_to_basic_graph(pi_qew_list, distance)
    NB += 1
    return {KEY: NB, AVERAGE_DISTANCE: (0, 1, 0, 0, 0), NEIGHBORS: [], POINTS: pi_qew_list, TYPE: LEAF}


def from_pi_node_to_basic_graph(pi_node, distance):
    global NB
    the_sons = []
    the_points = []
    for tree_node in pi_node[1:]:
        graph_node = from_pi_qew_tree_to_basic_graph(tree_node, distance)
        the_sons.append(graph_node)
        the_points.extend(graph_node[POINTS])
    NB += 1
    return {KEY: NB, AVERAGE_DISTANCE: average_distance(the_sons, distance),
            NEIGHBORS: the_sons, POINTS: the_points, TYPE: P_NODE}


def average_distance(node_list, distance):
    distance_sum = 0
    distance_number = 0
    distance_max = 0
    distance_min = float('inf')
    ensemble = []
    for i in range(len(node_list)):
        for j in range(i + 1, len(node_list)):
            for point_i in node_list[i][POINTS]:
                for point_j in node_list[j][POINTS]:
                    distance_sum += distance[point_i][point_j]
                    distance_number += 1
                    ensemble.append(distance[point_i][point_j])
                    if distance[point_i][point_j] > distance_max:
                        distance_max = distance[point_i][point_j]
                    if distance[point_i][point_j] < distance_min:
                        distance_min = distance[point_i][point_j]
    return distance_sum, distance_number, distance_max, distance_min, median(ensemble)


def from_qew_node_to_basic_graph(qew_node, distance):
    global NB
    basic_nodes = []
    all_points = []
    for node in qew_node[1:]:
        basic_nodes.append(from_pi_qew_tree_to_basic_graph(node, distance))
        all_points.extend(basic_nodes[-1][POINTS])
    current_nodes = basic_nodes
    height = 0
    while len(current_nodes) > 1:
        new_nodes = []
        height += 1
        n = len(current_nodes)
        for i in range(n - 1):
            k = i + height
            NB += 1
            the_new_node = {KEY: NB, NEIGHBORS: [current_nodes[i], current_nodes[i + 1]], POINTS: all_points,
                            TYPE: Q_NODE, REPRESENTS: [basic_nodes[i], basic_nodes[k]],
                            AVERAGE_DISTANCE: average_distance([basic_nodes[i], basic_nodes[k]], distance)}
            new_nodes.append(the_new_node)
        current_nodes = new_nodes

    return current_nodes[0]


""" ####################################################################################### """


def from_basic_graph_to_adjacency_list(basic_graph):
    size = basic_graph[KEY]
    adjacency_list = list(range(size + 1))
    recursive_from_basic_graph_to_adjacency_list(basic_graph, adjacency_list)


def recursive_from_basic_graph_to_adjacency_list(basic_graph, adjacency_list):
    line_nb = basic_graph[KEY]
    if type(adjacency_list[line_nb]) == int:
        adjacency_list[line_nb] = {AVERAGE_DISTANCE: basic_graph[AVERAGE_DISTANCE]}
        adjacency_list[line_nb][NEIGHBORS] = []
        for node in basic_graph[NEIGHBORS]:
            adjacency_list[line_nb][NEIGHBORS].append(node[KEY])
            recursive_from_basic_graph_to_adjacency_list(node, adjacency_list)


"""#######################################################################################"""


def calculate_position_vector(p, node, position):
    global NB
    new_position = position
    if p == 1:
        median_to_use = node[AVERAGE_DISTANCE][4]
        new_position.append((NB, median_to_use))

    if p == 2:
        mean = node[AVERAGE_DISTANCE][0] / node[AVERAGE_DISTANCE][1]
        new_position.append((NB, mean))

    if p == 'inf':
        min_max = (node[AVERAGE_DISTANCE][2] + node[AVERAGE_DISTANCE][3]) / 2
        new_position.append((NB, min_max))

    return new_position


"""#######################################################################################"""


def from_pi_qew_tree_to_basic_graph_with_position_and_weight(pi_qew_list, distance, norme=1):
    global NB
    position = []
    weight = []
    if pi_qew_list[0] == P_NODE:
        return from_pi_node_to_basic_graph_with_position_and_weight(pi_qew_list, distance, position, weight, norme)
    if pi_qew_list[0] == Q_NODE:
        return from_qew_node_to_basic_graph_with_position_and_weight(pi_qew_list, distance, position, weight, norme)
    NB += 1
    position += [(NB, 0)]
    weight += [(NB, 1)]
    return {KEY: NB, AVERAGE_DISTANCE: (0, 1, 0, 0, 0), NEIGHBORS: [], POINTS: pi_qew_list,
            TYPE: LEAF}, position, weight


def from_pi_node_to_basic_graph_with_position_and_weight(pi_node, distance, position=None, weight=None, norme=1):
    if weight is None:
        weight = []
    if position is None:
        position = []
    global NB
    the_sons = []
    the_points = []
    for tree_node in pi_node[1:]:
        graph_node_with_position_and_weight = from_pi_qew_tree_to_basic_graph_with_position_and_weight(tree_node,
                                                                                                       distance, norme)
        graph_node = graph_node_with_position_and_weight[0]
        position += graph_node_with_position_and_weight[1]
        weight += graph_node_with_position_and_weight[2]
        the_sons.append(graph_node)
        the_points.extend(graph_node[POINTS])
    NB += 1
    pi_node = {KEY: NB, AVERAGE_DISTANCE: average_distance(the_sons, distance),
               NEIGHBORS: the_sons, POINTS: the_points, TYPE: P_NODE}
    position = calculate_position_vector(norme, pi_node, position)
    weight += [(NB, pi_node[AVERAGE_DISTANCE][1])]
    return pi_node, position, weight


def from_qew_node_to_basic_graph_with_position_and_weight(qew_node, distance, position=None, weight=None, norme=1):
    if weight is None:
        weight = []
    if position is None:
        position = []
    global NB
    basic_nodes = []
    all_points = []
    for node in qew_node[1:]:
        basic_nodes_with_position_and_weight = from_pi_qew_tree_to_basic_graph_with_position_and_weight(node, distance,
                                                                                                        norme)
        basic_nodes.append(basic_nodes_with_position_and_weight[0])
        position += basic_nodes_with_position_and_weight[1]
        weight += basic_nodes_with_position_and_weight[2]
        all_points.extend(basic_nodes[-1][POINTS])
    current_nodes = basic_nodes
    height = 0
    while len(current_nodes) > 1:

        new_nodes = []
        height += 1
        n = len(current_nodes)
        for i in range(n - 1):
            k = i + height
            NB += 1
            the_new_node = {KEY: NB, NEIGHBORS: [current_nodes[i], current_nodes[i + 1]], POINTS: all_points,
                            TYPE: Q_NODE, REPRESENTS: [basic_nodes[i], basic_nodes[k]],
                            AVERAGE_DISTANCE: average_distance([basic_nodes[i], basic_nodes[k]], distance)}
            new_nodes.append(the_new_node)
            position = calculate_position_vector(norme, the_new_node, position)
            weight += [(NB, the_new_node[AVERAGE_DISTANCE][1])]
        current_nodes = new_nodes

    return current_nodes[0], position, weight


def taking_only_coordinates(vector):
    coordinates = []
    for tuples in vector:
        coordinates += [tuples[1]]
    return coordinates
