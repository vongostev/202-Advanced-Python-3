import parser
import sympy
from sympy.abc import a, b, y

if __name__ == '__main__':
    parse_obj: parser.Parser = parser.Parser("ex.tex")
    for row in parse_obj.parse():
        expr = sympy.Eq(*map(sympy.sympify, row.split("=")))
        print(expr.subs([(a, 2), (y, 4), (b, 1)]))
