import sympy as sp
import string

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
                         'Ω', 'ω']
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
                       '\\omega']
greek_dict = dict(zip(latex_greek_letters, unicode_greek_letters))


def check_greek_letter(line: str):
    for letter in latex_greek_letters:
        while letter in line:
            line = line.replace(letter, greek_dict[letter])
    return line


def read_formula(line, border='', border2=''):
    """
    This function read given line
    (consider only case when at the beginning there is variable,
    then '=', then expression) and change some LaTeX syntax
    (merged letters in multiplication,
    \dfrac{}{} for fraction) for SymPy's recogntion.
    Return SymPy expression for given variable.
    """

    # Find greek letter and change it to the unicode greek letter
    line = check_greek_letter(line)

    for letter in latex_greek_letters:
        while letter in line:
            line = line.replace('\\phi', 'φ')

    # Check if there is a fraction and replace \dfrac{...}{...} to .../...
    if '\\frac{' in line:
        i = line.find('\\frac{')
        line = line.replace('\\frac{', '')
        j = line.find('}', i)
        k = line.find('}', j + 2)
        line = line[:j] + '/' + line[j + 2:k] + line[k + 1:]

    # Check if there is multiplication if variables
    for i in range(len(line) - 1):
        if (line[i] in string.ascii_lowercase and line[i + 1] in string.ascii_lowercase) or \
                (line[i] in unicode_greek_letters and line[i + 1] in unicode_greek_letters):
            line = line[:i + 1] + '*' + line[i + 1:]

    if border:
        i = line.find(border)
        variable = sp.sympify(line[i + len(border):line.find('=')])
        expression = sp.sympify(line[line.find('=') + 1:line.find(border2, i + len(border))])
        variable = expression
    else:
        variable = sp.sympify(line[:line.find('=')])
        expression = sp.sympify(line[line.find('=') + 1:])
        variable = expression
    print(variable)
    return variable


path = 'latex_example.tex'
with open(path, 'r') as f:
    for line in f:
        line = line.strip()
        if '$$' in line:
            read_formula(line, '$$', '$$')
        elif '$' in line:
            read_formula(line, '$', '$')
        elif '\\begin{equation}' in line:
            line = f.readline().strip()
            read_formula(line)
