from Main.foreign_program.Matrix_Construction_and_Modification import *
from Main.Program.linear_programmation import change_format_of_pi_qwe_list, make_isotonic_for_l_1, \
    make_round_on_matrix, print_matrix, make_isotonic_for_l_inf

a = geographic_distance(6,3,1,10)
print_matrix(a[0])
b = change_format_of_pi_qwe_list(a[1])
make_isotonic_for_l_inf(b,a[0])
make_round_on_matrix(a[0])
print_matrix(a[0])

