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
















