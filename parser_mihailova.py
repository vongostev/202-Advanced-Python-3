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

def change_formula(line: str):

    '''Замена дроби'''
    while('\\frac{' in line):
        left_num = line.find('\\frac{')
        right_num = line.find('}', left_num)
        right_denum = line.find('}', right_num + 2)
        line = line[:left_num] + line[(left_num + 6):right_num] + \
            ' / ' + line[(right_num + 2):right_denum] + \
            line[(right_denum + 1):]
        
    '''Замена греческих букв'''
    for greek_letter in latex_greek:
        while greek_letter in line:
            line = line.replace(greek_letter, greek_dict[greek_letter])

    '''Замена уножения'''
    length = len(line)
    i = 1
    while(i < length):
        if (line[i] in all_symbols_string and line[i - 1] in (all_symbols_string + '1234567890')):
            line = line[:i] + '*' + line[i:]
            length += 1
        i += 1

    '''Делаем замену для sympy'''
    if line.find('=') != -1:
        left_of_equation = sympy.sympify(line[:line.find('=')])
        right_of_equation = sympy.sympify(line[(line.find('=') + 1):])
        print(f'{left_of_equation} = {right_of_equation}')
    else:
        equation = sympy.sympify(line)
        print(equation)


if __name__ == "__main__":
    
with open('varya.tex', 'r') as file:
    for line in file:
        if '\\begin{equation}' in line:
            left_side = line.find('\\begin{equation}') + 16
            right_side = line.find('\\end{equation}', left_side)
            change_formula(line[left_side:right_side])
            line = line[:(left_side - 16)] + line[(right_side + 14):]
        if '$' in line and not('$$' in line):
            left_side = line.find('$') + 1
            right_side = line.find('$', left_side)
            change_formula(line[left_side:right_side])
            line = line[:(left_side - 1)] + line[(right_side + 1):]
        if '$$' in line:
            left_side = line.find('$$') + 2
            right_side = line.find('$$', left_side)
            change_formula(line[left_side:right_side])