import unittest
from collections.abc import Iterable
from simple_atm_controller.atm_controller import AtmController


class AtmControllerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        class TestAtmController(AtmController):
            def find_accounts_query(self, pin_number) -> Iterable:
                return ["A0001", "A0002", "A0003"]
            def get_valance_query(self, pin_number, account_id) -> int:
                return 10
            def update_valance_query(self, pin_number, account_id, dollar):
                pass

        self.controller = TestAtmController

    def test_allocate_atm_controller(self):
        self.controller()

    def test_invalid_atm_controller(self):
        class InvalidAtmController(AtmController):
            pass
        try:
            InvalidAtmController()
            self.assertTrue(False)
        except TypeError:
            pass

    
