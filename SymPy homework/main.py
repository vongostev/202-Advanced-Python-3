import sympy as sp
import string


def read_formula(line, border='', border2=''):
    """
    This function read given line
    (consider only case when at the beginning there is variable,
    then '=', then expression) and change some LaTeX syntax
    (merged letters in multiplication,
    \dfrac{}{} for fraction) for SymPy's recogntion.
    Return SymPy expression for given variable.
    """

    # Check if there is a fraction and replace \dfrac{...}{...} to .../...
    if '\\frac{' in line:
        i = line.find('\\frac{')
        line = line.replace('\\frac{', '')
        j = line.find('}', i)
        k = line.find('}', j + 2)
        line = line[:j] + '/' + line[j + 2:k] + line[k + 1:]

    # Check if there is multiplication if variables
    for i in range(len(line) - 1):
        if line[i] in string.ascii_lowercase and line[i + 1] in string.ascii_lowercase:
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
with open(path, 'r') as f:a
    for line in f:
        line = line.strip()
        if '$$' in line:
            read_formula(line, '$$', '$$')
        elif '$' in line:
            read_formula(line, '$', '$')
        elif '\\begin{equation}' in line:
            line = f.readline().strip()
            read_formula(line)
