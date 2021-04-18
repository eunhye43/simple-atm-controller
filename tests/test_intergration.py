import unittest, re
from collections.abc import Iterable
from simple_atm_controller.pin import PinValidationRule, Pin
from simple_atm_controller.account import Account
from simple_atm_controller.atm_controller import AtmController
from tests.data_model import DataBase


class IntergrationTestCase(unittest.TestCase):

    def setUp(self) -> None:

        class TestAtmController(AtmController):
            def find_accounts_query(self, pin_number) -> Iterable:
                return self.model.find_accounts(pin_number)
            def get_valance_query(self, pin_number, account_id) -> int:
                return self.model.get_valance(pin_number, account_id)
            def update_valance_query(self, pin_number, account_id, dollar):
                self.model.update_valance(pin_number, account_id, dollar)

        class CustomPinNumberRule(PinValidationRule):
            def validate(self, pin_number) -> bool:
                return bool(re.search(r"\d{2}-\d{2}", pin_number))

        self.model = DataBase
        self.controller = TestAtmController
        self.pin_rule = CustomPinNumberRule

    def test_check_valance(self):
        controller = self.controller(self.model())
        input_pin = "00-01"
        pin_number = Pin(input_pin)
        account1, account2 = controller.find_accounts(pin_number)
        account1_valance = controller.get_valance(account1)
        account2_valance = controller.get_valance(account2)
        self.assertEqual(account1_valance, 73)
        self.assertEqual(account2_valance, 23)

    def test_deposit_and_withdraw(self):
        controller = self.controller(self.model())
        src_pin, tgt_pin, dollar = "00-02", "00-00", 300
        src_account = controller.find_accounts(Pin(src_pin))[0]
        tgt_account = controller.find_accounts(Pin(tgt_pin))[0]
        controller.withdraw(src_account, dollar)
        controller.deposit(tgt_account, dollar)

        src_valance = controller.get_valance(src_account)
        tgt_valance = controller.get_valance(tgt_account)
        self.assertEqual(src_valance, 100_000 - 300)
        self.assertEqual(tgt_valance, 0 + 300)

    def test_minus_valance(self):
        controller = self.controller(self.model())
        account = controller.find_accounts(Pin("00-00"))[0]
        for dollar in range(1, 300):
            status, _ = controller.withdraw(account, dollar)
            self.assertFalse(status)
        valance = controller.get_valance(account)
        self.assertEqual(valance, 0)

    def test_user_non_exist(self):
        # Non-existent Pin
        controller = self.controller(self.model())
        non_exist_pin = Pin("00-99")
        accounts = controller.find_accounts(non_exist_pin)
        self.assertEqual(accounts, [])

        # Non-existent Account
        non_exist_account = Account(non_exist_pin, "Invalid")
        valance = controller.get_valance(non_exist_account)
        self.assertEqual(valance, None)
