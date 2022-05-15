import sympy.abc
import re
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
latex_greek = ['Alpha',
               'alpha',
               'Beta',
               'beta',
               'Gamma',
               'gamma',
               'Delta',
               'delta',
               'Epsilon',
               'epsilon',
               'Zeta',
               'zeta',
               'Eta',
               'eta',
               'Theta',
               'theta',
               'Iota',
               'iota',
               'Kappa',
               'kappa',
               'Lambda',
               'lambda',
               'Mu',
               'mu',
               'Nu',
               'nu',
               'Xi',
               'xi',
               'Omicron',
               'omicron',
               'Pi',
               'pi',
               'Rho',
               'rho',
               'Sigma',
               'sigma',
               'Tau',
               'tau',
               'Upsilon',
               'upsilon',
               'Phi',
               'phi',
               'Chi',
               'chi',
               'Psi',
               'psi',
               'Omega',
               'omega']

greek_dict = dict(zip(latex_greek, unicode_greek))


def healer(line: str):
    for greek_letter in latex_greek:
        while greek_letter in line:
            line = line.replace(greek_letter, greek_dict[greek_letter])


def parsing():
    with open('C:\\Users\\Ducky\\OneDrive\\Документы\\GitHub\\202-Advanced-Python-3\\test.txt') as f:
        formulas = list()
        for item in f:
            formulas.append(re.findall(
                r'\\begin{equation}(.*?)\\end{equation}', item))
            formulas.append(re.findall(r'\$([^$]+)\$', item))

    i = 0
    while i < len(formulas):
        if len(formulas[i]) == 0:
            formulas.pop(i)
            i -= 1
        i += 1

    for i in range(len(formulas)):
        formulas[i] = formulas[i][0].replace('\\', '')

        for greek_letter in latex_greek:
            while greek_letter in formulas[i]:
                formulas[i] = formulas[i].replace(
                    greek_letter, greek_dict[greek_letter])

        while (formulas[i].find('frac{') != -1):
            formulas[i] = formulas[i].replace('frac{', '(')
            formulas[i] = formulas[i].replace('}{', ')/(')
            formulas[i] = formulas[i].replace('}', ')')

        if (formulas[i].find('=') != -1):
            left = sympy.sympify(formulas[i][:formulas[i].find('=')])
            right = sympy.sympify(formulas[i][(formulas[i].find('=') + 1):])
            formulas[i] = (f'{left} = {right}')
        else:
            formulas[i] = sympy.sympify(formulas[i])

    print(formulas)
    return formulas


if __name__ == '__main__':
    data = parsing()
