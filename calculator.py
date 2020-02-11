#               #
# calculator.py #
#               #

import math
import random
# import scipy

'''
    TODO: 
 
    Idea with calculator: support other operations as well, all kinds of cool math and visualisation stuff
    like creating a diagram for a specified function oder something like that.

    Addition & Subtraction with + and -
    Multiplication and Division with * and /
    Exponentiation with ** and nth root of x with 'n r x'
    Floor Division and Modulo with // and %
    Factorial with ! and binomial coefficient (x over n) with 'x o n'
    Finding the greatest common divisor of x and y with 'x gcd y'
    Summing up a list of values with sum(val1, val2, val3, ..., valn) 
    Counting the amount of values in a series with count()
    sin sin(x), cos cos(x), tan tan(x), arcsin arcsin(x), arccos arccos(x), arctan arctan(x), 
    Finding the euclidean distance between two points with dist(p[x;y],q[x;y]).
    Finds the median med(), arithmetic mean mean(), mode mode(), geometric mean gmean(), harmonic mean hmean(), range range() and expected value ev().
    Skewness skew(), Kurtosis kurt(), Standard Deviation stdev(), Interquartile Range iqr(), Mean absolute difference madif(), Mean absolute deviation madev(), Variance var()
    Convert angle x from radians to degrees with deg() or vice versa with rad()
    Constants: pi, e, tau, c, G, h, L, k, electron mass me, proton mass mp, M, T, Q, golden ratio gr, 
    SHA1(), SHA256(), ... security functions and encryption
    Random numbers
    Intersections and derivatives of functions

'''

# Safe functions
safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau']

# Assign to dict
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])

# Safe builtins
safe_dict['abs'] = abs
safe_dict['bin'] = bin
safe_dict['chr'] = chr
safe_dict['complex'] = complex
safe_dict['divmod'] = divmod
safe_dict['enumerate'] = enumerate
safe_dict['hash'] = hash
safe_dict['hex'] = hex
safe_dict['len'] = len
safe_dict['min'] = min
safe_dict['max'] = max
safe_dict['map'] = map
safe_dict['oct'] = oct
safe_dict['ord'] = ord
safe_dict['pow'] = pow
safe_dict['range'] = range
safe_dict['reversed'] = reversed
safe_dict['round'] = round
safe_dict['sum'] = sum
safe_dict['zip'] = zip


user_expression = input("Input: ")

print(eval(user_expression,{"__builtins__":None}, safe_dict))
