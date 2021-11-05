
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpmath import *

mp.dps = 20

def fermi_dirac_function(exponent, value, x):
    mpfexponent = mp.mpmathify(exponent)
    mpfvalue = mp.mpmathify(value)
    mpfx = mp.mpmathify(x)
    mpfpoint1 = mp.mpmathify(1)
    mpfnumerator = mp.power( mpfx, mpfexponent )
    mpfsubstraction = mp.exp(mpfx - value)
    mpfdenominator = mpfpoint1 + mpfsubstraction
    return mpfnumerator / mpfdenominator

def fermi_dirac_function_no_exp(exponent, value, x):
    mpfexponent = mp.mpmathify(exponent)
    mpfvalue = mp.mpmathify(value)
    mpfx = mp.mpmathify(x)
    mpfnumerator = mp.power( mpfx, mpfexponent )
    mpfdenominator = mp.exp(mpfx) + mp.exp(value)
    return mpfnumerator / mpfdenominator * mp.mpmathify(2.0) / mp.sqrt(mp.pi)

def mplinspace(start, stop, num=50, endpoint=True):
    output = []
    mpfstart = mp.mpmathify(start)
    mpfstop = mp.mpmathify(stop)
    delta = mp.fsub(mpfstop, mpfstart)
    div = num
    for x in range(0, (div + 1) if endpoint else div):
        mpfx = mp.mpmathify(x)
        mpfdiv = mp.mpmathify(div)
        mpfdelta = mp.mpmathify(delta)
        accumulated = (mpfstart * mpfdiv + mpfx * mpfdelta) / mpfdiv
        output.append(accumulated)
    return output

def mid_point_search_fermi_dirac_no_exp(value_objective = mp.mpmathify(0.5), value_min = mp.mpmathify(-1e3), value_max = mp.mpmathify(+1e5), print_values = False ):
    mpf_value_objective = value_objective
    mpf_value_min = value_min
    mpf_value_max = value_max
    value_half_point = value_max + (value_min - value_max)/mp.mpmathify(2)
    result_desired_half_point = mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), value_half_point, x), [0, mp.inf])

    while not mp.almosteq(result_desired_half_point, value_objective):
        if value_objective >= result_desired_half_point:
            value_max = value_half_point
        else:
            value_min = value_half_point

        value_half_point = value_max + (value_min - value_max)/mp.mpmathify(2)
        result_desired_half_point = mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), value_half_point, x), [0, mp.inf])
        if print_values:
            print(value_max, value_min, result_desired_half_point, value_objective, value_half_point, mp.almosteq(result_desired_half_point, value_objective))

    return value_half_point

import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

"""
Pruebas sueltas
"""
##### Cálculo de la función fermi dirac con diferentes valores
# print(mp.quad(lambda x: fermi_dirac_function(mp.mpmathify(1/2), 0, x), [0, mp.inf]))
# print(mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(0.5), 0, x), [0, mp.inf]))
##### Esta línea de aquí permite el cálculo de la función fermi dirac F1/2(x). El 0.5 representa el valor de qué Fermi es, el 0.1, el valor de x.
# print(mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(0.5), 0.1, x), [0, mp.inf]))
##### Esta línea de aquí permite el cálculo de la inversa de la función fermi dirac 1/2, (F1/2)^-1(x), dado el valor de entrada. F1/2 (0.1) = 0.748804375 ==> (F1/2)^-1(0.748804375) = 0.1
# print(mid_point_search_fermi_dirac_no_exp(value_objective = mpf('0.001'), print_values = True))
# print(mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), mpf('0'), x), [0, mp.inf]))
##### Pruebas con la función linspace
# for value in mplinspace(-40, 40, 800):
#     print(value)
#
# for value in mplinspace(-5, 0, 200, False):
#     print(value, mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), value, x), [0, mp.inf]))

"""
Medición estadística de tiempos
"""
pass
# import time
# import random
# import statistics
# timessigned = []
# for i in range(0,20):
#     starttit = time.perf_counter()
#     x = random.random()
#     y = mid_point_search_fermi_dirac_no_exp(value_objective = mpf(x), print_values = False)
#     endtit = time.perf_counter()
#     timessigned.append(endtit - starttit)
#     print(x, y, endtit - starttit)
#
# print(statistics.mean(timessigned),
#  statistics.pstdev(timessigned),
#  statistics.pvariance(timessigned),
#  statistics.stdev(timessigned),
#  statistics.variance(timessigned))


# def mid_point_search_fermi_dirac_no_exp_tests(value_objective = '0.5', value_min = '-1e5', value_max = '+1e5'):
#     mpf_value_objective = mpf(value_objective)
#     mpf_value_min = mpf(value_min)
#     mpf_value_max = mpf(value_max)
#     value_half_point = mpf_value_max + (mpf_value_min - mpf_value_max)/mp.mpmathify(2)
#     result_desired_half_point = mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), value_half_point, x), [0, mp.inf])
#     while not mp.almosteq(result_desired_half_point, value_objective):
#         if value_objective > result_desired_half_point:
#             value_max = value_half_point
#         else:
#             value_min = value_half_point
#         value_half_point = mpf_value_max + (mpf_value_min - mpf_value_max)/mp.mpmathify(2)
#         result_desired_half_point = mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), value_half_point, x), [0, mp.inf])
#         print(value_half_point, result_desired_half_point, value_max, value_min)
#     return value_half_point

# mpf_max_nested_1 = 1000
# mpf_max_nested_2 = 1000
# mpf_elements_range = mplinspace(mpf('0'), mpf('1'), mpf_max_nested_1, True)
# mpf_elements_per_range = mplinspace(mpf('0'), mpf('1'), mpf_max_nested_2, True)
#
# for i in range(len(mpf_elements_range)-2):
#     for j in range(len(mpf_elements_per_range)-1):
#         xvalue = mpf_elements_range[i+1] + mpf_elements_per_range[j] / mpf_max_nested_1
#         print(xvalue, mid_point_search_fermi_dirac_no_exp(value_objective = xvalue))
#         # print(mpf_elements_range[i+1], mpf_elements_per_range[j], xvalue)

"""
Para calcular la inversa de la función fermi 1/2
"""
previous_value = mpf('20')
previous_value = mid_point_search_fermi_dirac_no_exp(value_objective = mpf('0.001'), value_min = mpf('-20'), value_max = mpf('20'))
for value in range(0,10):
    # print(mpf('0.000001') + mpf(value) / mpf(10), mpf('0.1') + mpf(value) / mpf(10))
    # print(mpf('0.000001') + mpf(value) / mpf(10000), mpf('0.1') + mpf(value) / mpf(10000))
    mpf_elements = mplinspace(mpf('0.001') + mpf(value) / mpf(10), mpf('0.1') + mpf(value) / mpf(10), 99, False)
    # mpf_elements = mplinspace(mpf('0.000001') + mpf(value) / mpf(10000), mpf('0.1') + mpf(value) / mpf(10000), 99999, False)
    # eprint("value =", value)
    for value in mpf_elements:
        # pass
        actual_value = mid_point_search_fermi_dirac_no_exp(value_objective = value, value_min = previous_value - mpf('1'), value_max = previous_value)
        print(value, actual_value, file=sys.stderr)
        print(value, actual_value, file=sys.stdout)
        previous_value = actual_value
