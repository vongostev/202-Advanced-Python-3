# -*- coding: utf-8 -*-
"""
Created on Mon May 16 20:59:51 2022

@author: TH000
"""

import numpy as np
import math as ma
import matplotlib.pyplot as plt
import scipy.special as SCS
import time
import sympy as sy

def compilashon(line):
    line = line.replace('$', '')
    line_trial = ""
    i = 0
    for letters in latex_greek_letters:
        while letters in line:
            line = line.replace(letters, unicode_greek_letters[i])
        i += 1
    while('\\frac{' in line):
        frac = line.find('\\')
        line = line[:frac] + line[frac+5:]
        for i in [0, 1]:
            begin = line.find('{')
            end = line.find('}')
            if i == 0:
                line = line[:begin] + line[begin+1:end] + '/' + line[end + 1:]
                continue
            line = line[:begin] + line[begin+1:end] + line[end + 1:]
    k = 0
    while (line[k] == ' '):
        k += 1
    line = line.replace(' ', '', k)
    for k in np.arange(0, len(line) - 1):
        if (line[k] != " ") and line[k + 1] != " " and line[k] != "*" and line[k+1] != "/":
            line = line[:k+1] + '*' + line[k+1:]
    return line

unicode_greek_letters = ['Α', 'α',
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
                         'Ω', 'ω',
                         'φ']
latex_greek_letters = ['\\Alpha',
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
                       '\\omega',
                       '\\phi']

with open("proga.tex", "r") as f:
    data = f.read()
all_line = data.splitlines()
all_equation = np.array([])
for i in np.arange(len(all_line)):
    if '$' in all_line[i]:
        all_line[i] = compilashon(all_line[i])
        all_equation = np.append(all_equation, all_line[i])
        continue
    if '\\begin{equation}' in all_line[i]:
        all_line[i+1] = compilashon(all_line[i+1])
        all_equation = np.append(all_equation, all_line[i+1])
for i in np.arange(len(all_equation)):
    u = sy.sympify(all_equation[i][4:])
    print(u)