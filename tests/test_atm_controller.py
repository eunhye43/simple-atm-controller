import unittest
from collections.abc import Iterable
from simple_atm_controller.atm_controller import AtmController
from simple_atm_controller.pin_number import PinNumber
from simple_atm_controller.account_id import AccountId
from simple_atm_controller.exceptions import (
    AtmControllerInputException, AtmControllerQueryException
)


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
        self.pin_number = PinNumber("P0001")
        self.account_id = AccountId(self.pin_number, "A0001")

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

    def test_find_account(self):
        module = self.controller()
        testcase = [
            (self.pin_number, True),
            ("P0001", False),
            (11111, False),
        ]
        for pin_i, expect in testcase:
            try:
                accounts = module.find_accounts(pin_i)
                self.assertEqual(True, expect)
                for account_i in accounts:
                    self.assertTrue(isinstance(account_i, AccountId))
                    self.assertEqual(account_i.pin_number, pin_i.pin_number)
            except AtmControllerInputException:
                self.assertEqual(False, expect)

    def test_invalid_find_account_query(self):

        class InvalidController(self.controller):
            def find_accounts_query(self, pin_number):
                return True

        module = InvalidController()
        try:
            module.find_accounts(self.pin_number)
            self.assertTrue(False)
        except AtmControllerQueryException:
            pass

    def test_get_valance(self):
        module = self.controller()
        testcase = [
            (self.account_id, True),
            (self.pin_number, False),
            ("P0001", False),
            (11111, False),
        ]
        for account_i, expect in testcase:
            pass

