#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures
import time
from itertools import repeat
import copy

import sys

from mpmath import *

mp.dps = 20
mp.pretty = False

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
    if print_values:
        print(f'Searching {value_objective} between {value_max} and {value_min}...')
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


def fermi_12_ex(value):
    mpf_value = mp.mpmathify(value)
    return mp.quad(lambda x: fermi_dirac_function_no_exp(mp.mpmathify(1/2), mpf_value, x), [0, mp.inf])

def searcher_greater_than_ex(value, objective):
    # nprint(result, mp.dps)
    return value >= objective

def parallel_fermi_12(values):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        evaluation = executor.map(fermi_12_ex, values)
        output_results = list(evaluation)
        return output_results

def parallel_searcher_greater_than(input_data, value_target):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        objective_results = executor.map(lambda x:searcher_greater_than_ex(x, value_target), input_data)
        output_results = list(objective_results)
        return output_results

def main():
    basic_values = mplinspace(-0.9999, 1, 6, False)
    for value in basic_values:
        nprint(value, mp.dps)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for results, basic_values in zip(executor.map(lambda x:mid_point_search_fermi_dirac_no_exp(value_objective=x, print_values=False), basic_values)):
            nprint(result, mp.dps)
            nprint(basic_values, mp.dps)

if __name__ == '__main__':
    main()
