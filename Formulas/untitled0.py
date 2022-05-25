# -*- coding: utf-8 -*-
"""
Created on Wed May 25 02:19:00 2022

@author: uclap
"""

import sympy
#import numpy as np

LatexDict = [[],[]]
LatexDict[0] = [
            'Alpha',    'alpha',
            'Beta',     'beta',
            'Gamma',    'gamma',
            'Delta',    'delta',
            'Epsilon',  'epsilon',
            'Zeta',     'zeta',
            'Eta',      'eta',
            'Theta',    'theta',
            'Iota',     'iota',
            'Kappa',    'kappa',
            'Lambda',   'lambda',
            'Mu',       'mu',
            'Nu',       'nu',
            'Xi',       'xi',
            'Omicron',  'omicron',
            'Pi',       'pi',
            'Rho',      'rho',
            'Sigma',    'sigma',
            'Tau',      'tau',
            'Upsilon',  'upsilon',
            'Phi',      'phi',
            'Chi',      'chi',
            'Psi',      'psi',
            'Omega',    'omega'
    ]
LatexDict[1] = [
            'Α', 'α',
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
            'Ω', 'ω'
            ]

NotLettersDict = '+-*/=^_()'


def fixformulafrac(formula):
    while('\\frac{' in formula):
        left_num = formula.find('\\frac{')
        rigth_num = formula.find('}', left_num)
        rigth_denum = formula.find('}', rigth_num + 2)
        formula = formula[:left_num] + '(' + formula[(left_num + 6):rigth_num] + ') / (' + formula[(rigth_num + 2):rigth_denum]  + ')' + formula[(rigth_denum + 1):]
    return formula
def fixformulaspace(formula):
    formula = formula.replace(" ", "")
    return formula
def fixformulamul(formula):
    for i in range(len(formula) - 1):
        if (formula[i] not in NotLettersDict) and (formula[i + 1] not in NotLettersDict) :
            formula = formula[:i + 1] + "*" + formula[i + 1:]
    #print("Fixed multiplication formula: ", formula)
    return formula
def fixformula(formula):
    for i in range(len(LatexDict[0])):
        while(formula.find(LatexDict[0][i]) > -1):
            formula = formula.replace("\\" + LatexDict[0][i], LatexDict[1][i])
    #print("Fixed formula: ", formula)
    return formula

def recognize(formula):
    formula = fixformulaspace(formula)
    formula = fixformulafrac(formula)
    formula = fixformula(formula)
    formula = fixformulamul(formula)
    Sformula = sympy.sympify(formula)
    print("Recognized formula: ", Sformula.subs(0, 0))
    return Sformula
    

def ExportFormulasFromLatexFile(filename):
    Formulas = []
    with open(filename, 'r') as file:
        data = file.readlines();
        #print(data)
        for string in data:
            trigger = False
            
            n = 0
            n1 = string.find('$', 0)
            n2 = n1
            while(True):
                n += 1
                n2 = n1
                n1 = string.find('$' , n)
                if(n1 == -1):
                    break
                if(abs(n1 - n2) > 1):
                    string = string[n2 + 1:][:n1 - n2 - 1]
                    strings = string.split('=')
                    print(strings)
                    for formula in strings:
                        recognize(formula)
                


if __name__ == "__main__":
    ExportFormulasFromLatexFile('Latex.tex')
