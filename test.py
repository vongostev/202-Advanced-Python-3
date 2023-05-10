import unittest
from course_py import*

#Тесты 
# 1)Когда структура состоит только из сверхпроводника, дельта = дельта0
# 2)Проверка, что сверхпроводнику не присвоено какое-то значение обменной энергии Н
# 3)Проверка значения температуры при определенных параметрах системы 
class Testf(unittest.TestCase):
    def test_convergence(self):
        a = (0, 1, 1, 1, 1, 1, 1, 100)
        b = (0, 0, 0, 0, 0, 0, 0, 0)
        sconductor = Material(a)
        ferro = Material(b)
        T = 0.8
        Del0 = selfcons0(T, sconductor.Tc)
        Del = selfcons(Del0, T, sconductor, ferro)
        x = (abs(Del[1].real-Del0) <= 0.001)
        self.assertTrue(x)

    def test_H(self):
        sconductor, ferro = f_read('D:\python\config.txt')
        self.assertEqual(sconductor.H, 0)

    def test_value(self):
        a = (0, 1, 1, 1.236, 1, 1, 0.3, 100)
        b = (18.57, 0.854, 8, 1.124, 0, 0, 0, 100)
        sconductor = Material(a)
        ferro = Material(b)
        x = (f(sconductor, ferro) - 0.565) <= 0.001
        self.assertTrue(x)
        
        
    

if __name__ == "__main__":
    unittest.main()