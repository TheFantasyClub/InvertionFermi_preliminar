
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures

from mpmath import *

mp.dps = 20
mp.pretty = False

def fermi_dirac_function_no_exp(exponent, value, x):
    mpfexponent = mpmathify(exponent)
    mpfvalue = mpmathify(value)
    mpfx = mpmathify(x)
    mpfnumerator = power( mpfx, mpfexponent )
    mpfdenominator = exp(mpfx) + exp(value)
    return mpfnumerator / mpfdenominator * mpmathify('2.0') / sqrt(mp.pi)


def mplinspace(start, stop, num=50, startpoint=True, endpoint=True):
    output = []
    mpfstart = mpmathify(start)
    mpfstop = mpmathify(stop)
    delta = fsub(mpfstop, mpfstart)
    div = num
    for x in range(0 if startpoint else 1, (div + 1) if endpoint else div):
        mpfx = mpmathify(x)
        mpfdiv = mpmathify(div)
        mpfdelta = mpmathify(delta)
        accumulated = (mpfstart * mpfdiv + mpfx * mpfdelta) / mpfdiv
        output.append(accumulated)
    return output


def fast_calculation_root(point = 0):
    precision_previous = mp.dps
    mp.dps = 3
    basic_value_near_fast = findroot(lambda x: quad(lambda y: fermi_dirac_function_no_exp(mpmathify(1/2), x, y), [0, inf])-mpmathify(point), (-100, 100), solver='bisect')
    value_near_min = basic_value_near_fast - mpmathify(0.01)
    value_near_max = basic_value_near_fast + mpmathify(0.01)
    mp.dps = precision_previous
    return findroot(lambda x: quad(lambda y: fermi_dirac_function_no_exp(mpmathify(1/2), x, y), [0, inf])-mpmathify(point), (value_near_min, value_near_max), solver='ridder')


def main():
    basic_values = mplinspace(0, 1, 6, False, False)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for value in basic_values:
            future = executor.submit(fast_calculation_root, value)
            print(nstr(future.result(), mp.dps), nstr(value, mp.dps))


if __name__ == '__main__':
    main()
