import sympy
import einsteinpy
import Program
import unittest


class TestWritingMethods(unittest.TestCase):

    def test_file_creation(self):
        output_object = Program.Output_Object('.\Tests.txt')
        output_object.end()
        with open('.\Tests.txt', mode='r', encoding='utf-8') as output_file:
            for s in output_file:
                None
        self.assertEqual(s, '\end{document}\n')

    def test_write(self):
        output_object = Program.Output_Object('.\Tests.txt')
        output_object.write('Гостев вредный и ... просто вредный.\n')
        with open('.\Tests.txt', mode='r', encoding='utf-8') as output_file:
            for s in output_file:
                None
        self.assertEqual(s, 'Гостев вредный и ... просто вредный.\n')

    # Проверяет число независимых компонент, выведенных в файл.
    def test_write_riemann(self):
        pre_metric = [[0 for i in range(4)] for k in range(4)]
        pre_metric[0][0] = - 1
        pre_metric[1][1] = 1
        pre_metric[2][2] = 1
        pre_metric[3][3] = 1
        coordinates = sympy.symbols('t x y z')
        metric_covariant = einsteinpy.symbolic.MetricTensor(
            pre_metric, coordinates)
        riemann_curvature = einsteinpy.symbolic.riemann.RiemannCurvatureTensor.from_metric(
            metric_covariant)
        riemann_curvature = riemann_curvature.change_config(newconfig='llll')
        riemann_curvature.simplify()
        output_object = Program.Output_Object('.\Tests.txt')
        output_object.write_riemann(riemann_curvature.tensor(), coordinates)
        with open('.\Tests.txt', mode='r', encoding='utf-8') as output_file:
            key_I = False
            n = 0
            for s in output_file:
                if s == '\\begin{document}\n':
                    key_I = True
                if key_I and ('0' in set(s)):
                    n += 1
        # 20 независимых компонент и один нуль из тождества Бианки.
        self.assertEqual(n, 21)


if __name__ == '__main__':
    unittest.main()
