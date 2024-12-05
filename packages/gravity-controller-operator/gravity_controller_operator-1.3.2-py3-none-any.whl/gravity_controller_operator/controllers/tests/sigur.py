from gravity_controller_operator.controllers.sigur import Sigur
import unittest


class TestCase(unittest.TestCase):
    controller = Sigur(ip="localhost")

    def test_di(self):
        di_response = self.controller.di_interface.get_dict()
        relay_response = self.controller.relay_interface.get_dict()
        print("relay_response", relay_response)

if __name__ == "__main__":
    unittest.main()