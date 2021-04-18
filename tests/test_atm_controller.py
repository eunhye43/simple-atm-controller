import unittest
from collections.abc import Iterable
from simple_atm_controller.atm_controller import AtmController
from simple_atm_controller.pin import Pin
from simple_atm_controller.account import Account
from simple_atm_controller.exceptions import (
    AtmControllerInputException,
    AtmControllerQueryException,
    AtmControllerException
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
        self.pin_number = Pin("P0001")
        self.account_id = Account(self.pin_number, "A0001")

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
                    self.assertTrue(isinstance(account_i, Account))
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
            try:
                module.get_valance(account_i)
                self.assertEqual(expect, True)
            except AtmControllerInputException:
                self.assertEqual(expect, False)

    def test_invalid_get_valance_query(self):

        class InvalidController(self.controller):
            def get_valance_query(self, pin_number, account_id) -> int:
                return "True"

        module = InvalidController()
        try:
            module.get_valance(self.account_id)
            self.assertTrue(False)
        except AtmControllerQueryException:
            pass

    def test_deposit(self):
        module = self.controller()
        testcase = [
            (self.account_id, 100, "success"),
            (self.account_id, 0, "success"),
            (self.pin_number, 100, "input_exception"),
            ("P0001", 100, "input_exception"),
            (11111, 100, "input_exception"),
            (self.account_id, "100", "input_exception"),
            (self.account_id, -100, "exception"),
        ]

        for account_i, dollar, expect in testcase:
            try:
                module.deposit(account_i, dollar)
                self.assertEqual(expect, "success")
            except AtmControllerInputException:
                self.assertEqual(expect, "input_exception")
            except AtmControllerException:
                self.assertEqual(expect, "exception")

    def test_withdraw(self):
        module = self.controller()
        testcase = [
            (self.account_id, 10, "success", True),
            (self.account_id, 0, "success", True),
            (self.account_id, 11, "success", False),
            (self.account_id, 100, "success", False),
            (self.pin_number, 10, "input_exception", False),
            ("P0001", 10, "input_exception", False),
            (11111, 10, "input_exception", False),
            (self.account_id, "100", "input_exception", False),
            (self.account_id, -10, "exception", False),
        ]

        for account_i, dollar, expect, expect_status in testcase:
            try:
                result_status, _ = module.withdraw(account_i, dollar)
                self.assertEqual(expect, "success")
                self.assertEqual(expect_status, result_status)
            except AtmControllerInputException:
                self.assertEqual(expect, "input_exception")
            except AtmControllerException:
                self.assertEqual(expect, "exception")

