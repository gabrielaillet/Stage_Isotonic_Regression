__author__ = 'pascal'

"""
Contains the functions:

logarithm(number, basis)
    "number" and "basis" are positive integers ("basis" > 1).
    returns an approximate integer value of log("number") in base "basis".
    works on 'very big' numbers.

put_off_singletons
    given list of lists (or sets, or tuples) "set_of_lists",
    returns the list of lists (or sets, or tuples) of "set_of_lists" of length > 1

sort_indices_by_values(indices, values)
    given two lists of same length 'n' "indices" and "values", sort, in exactly the same way, the two lists
    such that "values" is in increasing order
    works on site and in time O(n log(n)) -- is an implementation of heap-sort

sort_the_end_by_values(indices, values):
    identical to the previous function, except that the list "values" is sorted from the index 1.
    indices[0] and values[0] are neither considered nor changed.

reverse_end_of_list(the_list):
    given a list "the_list", reverse, on site, the_list[1:]

list_fusion(list_1, list_2)
    given two ordered lists "list_1" and "list_2", returns their fusion

transform_matrix_into_vector(matrix)

suppression_of_identical_lines(matrix)

distance_between_matrices(matrix_1, matrix_2)
    Given two matrices "matrix_1" and "matrix_2" of the SAME size (if not same size, big risk of error),
    returns a triple made of the L-infinite, L1 and L2 distances between "matrix_1 and "matrix_2".
    USES THE LIBRARY math.

transpose_matrix(matrix):
    returns the transpose of matrix "matrix"
    USES THE FUNCTION build_random_matrix

build_random_matrix(nb_lines, nb_columns, max_value):
    returns a random matrix on {0,.., "max_value"} with "nb_lines" lines, "nb_columns" columns

transforms_vector_into_zero_one(vector)
    Given a list of positive integers vector.
    Transform each value > 0 into 1

sorted_union(set_of_sets)
    Given a set of sets "set_of_sets", which is a list (or tuple or set) of lists (or tuples or sets),
    Return the union of these sets as a sorted tuple

point_suppression(removed_points, the_set)
    Given two ORDERED sets "removed_points" and "the_set", returns "the_set" \ "removed_points"

def transform_and_print_matrix_for_latex(the_matrix)
    Given a matrix "the_matrix", print each line 'i' for a cross table in the latex format such that the result is:
    i    X at place 'j' if "the_matrix[i][j]" > 0 and ' ' at place 'j' otherwise.
"""


import math
import random

from decimal import Decimal
INFINI = Decimal('Infinity')


def logarithm(number, basis):
    i = 0
    while number >= 1:
        i += 1
        number = number // basis
    return i


def put_off_singletons(set_of_lists):
    return [x for x in set_of_lists if len(x) > 1]


################################################################################################################

def sort_indices_by_values(indices, values):
    size = len(indices)
    for i in range((size + 1) // 2, -1, -1):
        heap_update(indices, values, i, size)
    for i in range(1, size):
        indices[0], indices[size - i] = indices[size - i], indices[0]
        values[0], values[size - i] = values[size - i], values[0]
        heap_update(indices, values, 0, size - i)


def heap_update(indices, values, rank, size):
    if (2 * rank) < size - 1:
        min_index = (2 * rank) + 1
        if min_index < size - 1 and values[min_index] < values[min_index + 1]:
            min_index += 1
        if values[rank] < values[min_index]:
            values[rank], values[min_index] = values[min_index], values[rank]
            indices[rank], indices[min_index] = indices[min_index], indices[rank]
            heap_update(indices, values, min_index, size)

################################################################################################################


################################################################################################################

def sort_the_end_by_values(indices, values):
    size = len(indices)
    for i in range((size + 1) // 2, 0, -1):
        end_heap_update(indices, values, i, size)
    for i in range(2, size):
        indices[1], indices[size + 1 - i] = indices[size + 1 - i], indices[1]
        values[1], values[size + 1 - i] = values[size + 1 - i], values[1]
        end_heap_update(indices, values, 1, size + 1 - i)


def end_heap_update(indices, values, rank, size):
    if (2 * rank) < size:
        min_index = 2 * rank
        if min_index < size - 1 and values[min_index] < values[min_index + 1]:
            min_index += 1
        if values[rank] < values[min_index]:
            values[rank], values[min_index] = values[min_index], values[rank]
            indices[rank], indices[min_index] = indices[min_index], indices[rank]
            end_heap_update(indices, values, min_index, size)

################################################################################################################


def reverse_end_of_list(the_list):
    for i in range(1, len(the_list) // 2):
        the_list[i], the_list[-i] = the_list[-i], the_list[i]


def list_fusion(list_one, list_two):
    from decimal import Decimal
    infinite = Decimal('Infinity')
    total_length = len(list_one) + len(list_two)
    the_list = []
    list_one = list_one + [infinite]
    list_two = list_two + [infinite]
    index_one = 0
    index_two = 0
    for i in range(total_length):
        if list_one[index_one] < list_two[index_two]:
            the_list.append(list_one[index_one])
            index_one += 1
        else:
            the_list.append(list_two[index_two])
            index_two += 1
    return the_list


def transform_matrix_into_vector(matrix):
    vector = []
    for line in matrix:
        vector.extend(line)
    return vector


def suppression_of_identical_lines(matrix):
    result = []
    for current_line in matrix:
        good = True
        for comparison_line in result:
            if comparison_line == current_line:
                good = False
                break
        if good:
            result.append(current_line)
    return result


def distance_between_matrices(matrix_1, matrix_2):
    maximum, summation, euclid = 0, 0, 0
    if len(matrix_1) > 0:
        for i in range(len(matrix_1)):
            for j in range(len(matrix_1[i])):
                difference = abs(matrix_1[i][j] - matrix_2[i][j])
                summation += difference
                euclid += difference ** 2
                if difference > maximum:
                    maximum = difference
    return [maximum, summation, math.sqrt(euclid)]


def transpose_matrix(matrix):
    if matrix is not None and len(matrix) > 0:
        nb_lines = len(matrix)
        nb_columns = len(matrix[0])
        result = build_random_matrix(nb_columns, nb_lines, 0)
        for i in range(nb_columns):
            for j in range(nb_lines):
                result[i][j] = matrix[j][i]
        return result


def build_random_matrix(nb_lines, nb_columns, max_value):
    line = [0] * nb_columns
    matrix = []
    for i in range(nb_lines):
        matrix.append(list(line))
    if max_value > 0:
        for i in range(nb_lines):
            for j in range(nb_columns):
                matrix[i][j] = random.randint(0, max_value)
    return matrix


def transforms_vector_into_zero_one(vector):
    for i in range(len(vector)):
        if vector[i] > 0:
            vector[i] = 1


def add_value_to_key_in_dictionary(value, key, dictionary):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value


def sorted_union(set_of_sets):
    result = set()
    for the_set in set_of_sets:
        result = result.union(set(the_set))
    the_list = list(result)
    the_list.sort()
    return tuple(the_list)


def point_suppression(removed_points, the_set):
    result = []
    removed_points.append(INFINI)
    i_removed, i_set = 0, 0
    while i_set < len(the_set):
        if the_set[i_set] != removed_points[i_removed]:
            result.append(the_set[i_set])
        if the_set[i_set] <= removed_points[i_removed]:
            i_removed += 1
        i_set += 1
    return result


def transform_and_print_matrix_for_latex(the_matrix):
    for i, line in enumerate(the_matrix):
        print (str(i) + " & " + (" & ".join([x and '$' + "\\" + "times$ " or "  " for x in line]) + '\\\\'))