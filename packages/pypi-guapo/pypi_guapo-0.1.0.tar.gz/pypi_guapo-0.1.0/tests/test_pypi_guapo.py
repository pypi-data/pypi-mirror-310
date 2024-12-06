import unittest
from pypi_guapo import hello_guapo

class TestPypiGuapo(unittest.TestCase):
    def test_hello_guapo(self):
        self.assertEqual(hello_guapo(), "Hello Guapo")

if __name__ == "__main__":
    unittest.main()
