import parser
from sympy.abc import a, b, y
import sympy.abc


def to_latex(data: list[str]):
    for i in range(len(data)):
        temp = data[i].replace('\\', '')
        data[i] = temp
    return data


if __name__ == '__main__':
    parse_obj: parser.Parser = parser.Parser("ex.tex")
    data = parse_obj.parse()
    data = to_latex(data)
    for row in data:
        expr = sympy.Eq(*map(sympy.sympify, (row.split("="))))
        print(expr.subs([(a, 2), (y, 4), (b, 1)]))
