import unittest
from solid3 import *


class TestCheckPath(unittest.TestCase):

    def test_positive_str(self):
        str_test = './test0.yaml'
        self.assertEqual(check_path(str_test), Path(str_test))

    def test_positive_path(self):
        path_test = Path('./test0.yaml')
        self.assertEqual(check_path(path_test), path_test)

    def test_exception_filenotfound(self):
        with self.assertRaises(FileNotFoundError):
            check_path('1')

    def test_exception_directory(self):
        with self.assertRaises(EnvironmentError):
            check_path('.')

    def test_exception_emptystr(self):
        with self.assertRaises(ValueError):
            check_path('')

    def test_exception_wrongtype(self):
        with self.assertRaises(AssertionError):
            check_path(10)


if __name__ == "__main__":
    unittest.main()
