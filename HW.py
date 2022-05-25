# -*- coding: utf-8 -*-
"""
Created on Wed May 25 01:39:47 2022

@author: grego
"""

import numpy as np
import sympy
import string

unicode_greek = ['Α', 'α',
                 'Β', 'β',
                 'Γ', 'γ',
                 'Δ', 'δ',
                 'Ε', 'ε',
                 'Ζ', 'ζ',
                 'Η', 'η',
                 'Θ', 'θ',
                 'Ι', 'ι',
                 'Κ', 'κ',
                 'Λ', 'λ',
                 'Μ', 'μ',
                 'Ν', 'ν',
                 'Ξ', 'ξ',
                 'Ο', 'ο',
                 'Π', 'π',
                 'Ρ', 'ρ',
                 'Σ', 'σ',
                 'Τ', 'τ',
                 'Υ', 'υ',
                 'Φ', 'φ',
                 'Χ', 'χ',
                 'Ψ', 'ψ',
                 'Ω', 'ω']

latex_greek = ['\\Alpha',
               '\\alpha',
               '\\Beta',
               '\\beta',
               '\\Gamma',
               '\\gamma',
               '\\Delta',
               '\\delta',
               '\\Epsilon',
               '\\epsilon',
               '\\Zeta',
               '\\zeta',
               '\\Eta',
               '\\eta',
               '\\Theta',
               '\\theta',
               '\\Iota',
               '\\iota',
               '\\Kappa',
               '\\kappa',
               '\\Lambda',
               '\\lambda',
               '\\Mu',
               '\\mu',
               '\\Nu',
               '\\nu',
               '\\Xi',
               '\\xi',
               '\\Omicron',
               '\\omicron',
               '\\Pi',
               '\\pi',
               '\\Rho',
               '\\rho',
               '\\Sigma',
               '\\sigma',
               '\\Tau',
               '\\tau',
               '\\Upsilon',
               '\\upsilon',
               '\\Phi',
               '\\phi',
               '\\Chi',
               '\\chi',
               '\\Psi',
               '\\psi',
               '\\Omega',
               '\\omega']

greek_dict = dict(zip(latex_greek, unicode_greek))

all_symbols_string = ''
for i in unicode_greek:
    all_symbols_string += i
all_symbols_string += string.ascii_letters

def change_greek(line: str):
    """
    latex greek -> unicode greek
    Parameters
    ----------
    line : str
    Returns
    -------
    line : str
    """
    for greek_letter in latex_greek:
        while greek_letter in line:
            line = line.replace(greek_letter, greek_dict[greek_letter])
    return line

def fractions(line: str):
    """
    frac{...}{...}
    Parameters
    ----------
    line : str
    Returns
    -------
    line : list of sympyfied left and right sides of equation
    """
    while('\\frac{' in line):
        left_num = line.find('\\frac{')
        rigth_num = line.find('}', left_num)
        rigth_denum = line.find('}', rigth_num + 2)

        line = line[:left_num] + line[(left_num + 6):rigth_num] + \
            ' / ' + line[(rigth_num + 2):rigth_denum] + \
            line[(rigth_denum + 1):]

    return line


def recognize_formula(line: str):

    line = change_greek(line)

    line = fractions(line)

    '''Changing {12ab} to {12*a*b}'''
    length = len(line)
    i = 1
    while(i < length):
        if (line[i] in all_symbols_string and line[i - 1] in (all_symbols_string + '1234567890')):
            line = line[:i] + '*' + line[i:]
            length += 1
        i += 1

    ''' Finally sympy expressions'''
    if line.find('=') != -1:
        left_of_equation = sympy.sympify(line[:line.find('=')])
        rigth_of_equation = sympy.sympify(line[(line.find('=') + 1):])
        # print(f'{left_of_equation} = {rigth_of_equation}')
        return [left_of_equation, rigth_of_equation]
    else:
        equation = sympy.sympify(line)
        return ['', equation]
        # print(equation)
















