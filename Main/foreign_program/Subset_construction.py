__author__ = 'pascal'

"""
Contains the functions:

ball_set(distance)
    Given a dissimilarity "distance" (on a set X (= {0,.. n-1})), returns a list made of all the balls of "distance"

ball_set_centered(line)
    Given a vector "line" (which represents distances of all elements of a set X to an element x of X), returns
    a list made of all the balls centered in x


ranked_balls_construction(distance, rank)
    Given a dissimilarity "distance" (on a set X (= {0,.. n-1})) and a maximum rank "rank", returns all the balls
    of "distance" of rank less than or equal to "rank".
    Used by robinson_recognition -- see the paper by PREA & FORTIN for the definition of the rank of the ball


two_ball_set(distance)
    Given a dissimilarity "distance" (on a set X (= {0,.. n-1})), returns a list made of all the two-balls of "distance"

two_ball(pt_a, pt_b, distance)
    Given a dissimilarity "distance" (on a set X (= {0,.. n-1})) and "pt_a" and "pt_b" in X, returns the two-ball of
    "pt_a" and "pt_b", i.e. the intersection of the two balls centered in "pt_a" and "pt_b" of
    radius "distance[pt_a][pt_b]"


delta_set(distance)
    Given a dissimilarity "distance", returns a list made of all the delta of "distance"

delta(pt_x, pt_y, distance)
    Given a dissimilarity "distance" on a set X (= {0,.. n-1}) and "pt_x" and "pt_y" in X, returns the delta of
    "pt_x" and "pt_y",i.e. the intersection, for all points 'pt' in X, of the balls centered in 'pt' and of
    radius max(distance[pt][pt_x], distance[pt][pt_y], distance[pt_x][pt_y].
    The delta of "pt_x" and "pt_y" is also the intersection of all the maximum cliques of "distance" which contain
    "pt_x" and "pt_y"


set_of_intervals_construction(points, nb_of_intervals)
    Given a set "points" (= {0, .. , n-1}) and a number " nb_intervals",
    Returns a list of "nb_of_intervals" intervals on "points"


set_of_noisy_intervals(points, nb_of_intervals)
    Given a set "points" (= {0, .. , n-1}) and a number " nb_intervals",
    Returns a list of "nb_of_intervals" 'noisy' intervals on "points"

noisy_interval(nb_points), first_point, end_point, slope_before, slope_after)
    Given the set {0, .. , "nb_points" -1})
    Returns a 'noisy interval' X on "points"; A point 'i' has probability of being in X:
        - 99.5 % if "first_point" <= i < "end_point"
        - max(1, 100 - (slope_before * ("first_point" - i)) % if i < "first_point"
        - max(1, 100 - (slope_after * (i - "end_point")) % if i >= "end_point",
    i.e. the probability of being in X is nearly 1 between "first_point" and "end_point", linearly decreases outside
    this interval, and is 1% outside the 'area of influence' of it.
    "first_point", "end_point", "slope_before" and "slope_after" are randomly generated.
    The percents 99.5 and 10 can be changed in the function "per_thousand"

from_presence_matrix_to_subsets(matrix)
    Given a 'presence matrix' "matrix" (i.e. a matrix where lines are indexed by 'objects' and columns by 'sites';
    on line 'i' and column 'j' is the number of objects 'i' found on site 'i').
    Returns a set of sets, represented as a list "set_of_subsets" of lists, with "set_of_subsets"[i] is the list of 'j'
    such that object 'i' has been fund on site 'j'.
"""


from Main.foreign_program.Diverse_Functions import sort_indices_by_values
from Main.foreign_program.Diverse_Functions import transform_matrix_into_vector

from decimal import Decimal
INFINI = Decimal('Infinity')

import random

from Main.foreign_program.Diverse_Functions import transpose_matrix
from Main.foreign_program.Diverse_Functions import transforms_vector_into_zero_one


##########################################################################

def ball_set(distance):
    the_ball_set = []
    for line in distance:
        small_ball_set = ball_set_centered(line)
        the_ball_set.extend(small_ball_set)
    return the_ball_set


def ball_set_centered(line):
    the_ball_set = []
    values = list(line)
    indices = list(range(len(line)))
    sort_indices_by_values(indices, values)
    for i in range(2, len(line)):
        if values[i - 1] != values[i]:
            the_ball_set.append(indices[: i])
    return the_ball_set

##########################################################################


#########################################################################

def ranked_balls_construction(distance, rank):
    neighbours = []
    for point in range(len(distance)):
        neighbours.append(neighbours_construction(point, rank, distance))
    return transform_matrix_into_vector(neighbours)


def neighbours_construction(point, rank, distance):
    n = len(distance)
    previous_min = -1
    neighbour = [[point]]
    val = [INFINI] * (rank + 1)
    for k in range(1, rank + 1):
        for y in range(n):
            if (point != y) and (previous_min < distance[point][y] < val[k]):
                val[k] = distance[point][y]
        previous_min = val[k]
    for k in range(1, rank + 1):
        neighbour.append([])
        for y in range(n):
            if distance[point][y] <= val[k]:
                neighbour[k].append(y)
    return neighbour

##########################################################################


##########################################################################

def two_ball_set(distance):
    the_two_ball_set = []
    for i in range(len(distance)):
        for j in range(i + 1, len(distance)):
            the_two_ball_set.append(two_ball(i, j, distance))
    return the_two_ball_set


def two_ball(pt_a, pt_b, distance):
    value = distance[pt_a][pt_b]
    the_two_ball = []
    for point in range(len(distance)):
        if distance[point][pt_a] <= value and distance[point][pt_b] <= value:
            the_two_ball.append(point)
    return the_two_ball

##########################################################################


##########################################################################

def delta_set(distance):
    the_delta_set = []
    for i in range(len(distance)):
        for j in range(i + 1, len(distance)):
            the_delta_set.append(delta(i, j, distance))
    return the_delta_set


def delta(pt_x, pt_y, distance):
    result = two_ball(pt_x, pt_y, distance)
    for pt_z in range(len(distance)):
        if len(result) == 2:
            break
        if pt_z != pt_x and pt_z != pt_y:
            value = max(distance[pt_x][pt_y], distance[pt_x][pt_z], distance[pt_y][pt_z])
            new_result = []
            for pt in result:
                if distance[pt][pt_z] <= value:
                    new_result.append(pt)
            result = new_result
    return result

###############################################################################


def set_of_intervals_construction(points, nb_of_intervals):
    set_of_intervals = []
    for i in range(nb_of_intervals):
        first_point = random.randint(0, len(points) - 2)
        end_point = random.randint(first_point + 1, len(points))
        set_of_intervals.append(points[first_point: end_point])
    return set_of_intervals


#################################################################################

def set_of_noisy_intervals(points, nb_of_intervals):
    set_of_intervals = []
    for i in range(nb_of_intervals):
        set_of_intervals.append(noisy_interval(len(points)))
    return set_of_intervals


def noisy_interval(nb_points):
    slope_min, slope_max = 100, 500
    first_point = random.randint(0, nb_points - 2)
    end_point = random.randint(first_point + 1, nb_points)
    slope_before, slope_after = random.randint(slope_min, slope_max), random.randint(slope_min, slope_max)
    interval = []
    for i in range(nb_points):
        if random.randint(0, 1000) < per_thousand(i, first_point, end_point, slope_before, slope_after):
            interval.append(i)
    return interval


def per_thousand(i, first_point, end_point, slope_before, slope_after):
    nb_max, nb_min = 995, 10
    if first_point <= i < end_point:
        return nb_max
    if i < first_point:
        return max(nb_min, nb_max - (slope_before * (first_point - i)))
    if i >= end_point:
        return max(nb_min, nb_max - (slope_after * (i - end_point)))

#################################################################################


def from_presence_matrix_to_subsets(matrix):
    set_of_subsets = []
    for line in matrix:
        subset = []
        for i in range(len(line)):
            if line[i] > 0:
                subset.append(i)
        set_of_subsets.append(subset)
    return set_of_subsets


def brute_data_from_alberti():
    return [[2, 5, 3, 0, 1, 0, 2, 4, 2, 1, 1, 2, 1, 3, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0, 0, 0, 1, 0, 1, 1, 0, 3, 0, 1, 0, 0, 0, 0],
            [0, 1, 4, 2, 2, 1, 1, 0, 0, 3, 2, 1, 0, 2, 0, 0, 0, 1, 1],
            [0, 1, 2, 1, 1, 0, 1, 1, 4, 3, 2, 2, 0, 6, 0, 3, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0],
            [1, 3, 1, 1, 1, 2, 2, 5, 4, 2, 1, 3, 0, 2, 0, 2, 0, 2, 1],
            [0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1, 2, 1, 0, 0, 0, 2, 0, 1],
            [1, 1, 2, 0, 1, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 3, 4, 3, 2, 2, 2, 4, 4, 2, 5, 5, 1, 7, 0, 0, 0, 1, 1],
            [1, 0, 0, 2, 1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [1, 3, 2, 1, 0, 0, 2, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
            [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 2, 0, 0, 1, 12, 3, 1, 0, 2, 1, 2, 0, 0, 0, 1, 0],
            [0, 4, 1, 0, 0, 0, 1, 3, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
            [0, 2, 2, 1, 0, 1, 2, 2, 2, 4, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
            [2, 2, 1, 2, 1, 1, 3, 4, 2, 1, 2, 3, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [2, 3, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [0, 2, 1, 0, 1, 0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 7, 0, 1, 6, 1, 7, 8, 5, 5, 6, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 3, 0, 2, 0, 0, 1, 1, 0, 3, 0, 4, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 12, 1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0]]


def suppress_some_points(data, points):
    for line in data:
        for i in range(len(line)):
            if i in points:
                line[i] = 0


def data_from_alberti(transpose=False):
    data = brute_data_from_alberti()

    suppress_some_points(data, [12, 14, 16, 15, 17, 5, 4, 10, 0])

    nb_points = len(data[0])
    if transpose:
        nb_points = len(data)
        data = transpose_matrix(data)
    result = []
    for line in data:
        partial_result = []
        for i in range(len(line)):
            if line[i] > 0:
                partial_result.append(i)
        result.append(partial_result)
    return [result, nb_points]
