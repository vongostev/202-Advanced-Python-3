import sympy.abc
import re


def parsing():
    with open('example.tex') as f:
        data = list(filter(None, f.read().split('\n')))
        formulas = list()
        for item in data:
            formulas.append(re.findall(r'\$\$(.*?)\$\$', item))
            formulas.append(re.findall(r'\\begin{equation}(.*?)\\end{equation}', item))
            #formulas.append(re.findall(r'\$([^$]+)\$', item))

    i = 0
    while i < len(formulas):
        if len(formulas[i]) == 0:
            formulas.pop(i)
            i -= 1
        i += 1

    for i in range(len(formulas)):
        for j in range(len(formulas[i])):
            temp = formulas[i][j].replace('\\', '')
            formulas[i][j] = temp
    print(formulas)
    return formulas


if __name__ == '__main__':
    data = parsing()
    for i in range(len(data)):
        for j in range(len(data[i])):
            expr = sympy.Eq(*map(sympy.sympify, (data[i][j].split("="))))
            print(expr)