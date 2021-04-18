"""
Example Code
    # check_valance() : Check the balance for the entered account
    # send_dollar() : Deposit and withdrawal sample code
"""
import re
from collections.abc import Iterable
from simple_atm_controller.pin import Pin, PinValidationRule
from simple_atm_controller.atm_controller import AtmController
from tests.data_model import DataBase


class MyAtmController(AtmController):
    """
    Overridden ATM Controller
    - You must specify the access method of the data model to the controller
    """

    def find_accounts_query(self, pin_number) -> Iterable:
        return self.model.find_accounts(pin_number)

    def get_valance_query(self, pin_number, account_id) -> int:
        return self.model.get_valance(pin_number, account_id)

    def update_valance_query(self, pin_number, account_id, dollar):
        self.model.update_valance(pin_number, account_id, dollar)


class CustomPinNumberRule(PinValidationRule):
    """
    PinNumber Validation Rule
    - Write a rule to verify the pin number
    """

    def validate(self, pin_number) -> bool:
        return bool(re.search(r"\d{2}-\d{2}", pin_number))


def check_valance():
    """Check the balance for the entered account"""
    print("Check Valance Output >> (00-00, shin10256)")

    # Input pin number
    input_pin = "00-01"
    # Pin number verification and objectification
    pin = Pin(input_pin, rule=CustomPinNumberRule())

    # Atm controller call and account selection
    CASH_BIN = DataBase()
    atm_controller = MyAtmController(CASH_BIN)
    accounts = atm_controller.find_accounts(pin)
    selected_account = accounts[0]

    # Print the current balance of the account
    print("%s's Valance: %s \n" % (
        selected_account,
        atm_controller.get_valance(selected_account)
    ))


def send_dollar():
    """Deposit and withdrawal sample code"""
    print("Send Dollar Output >> shino1025 => shin102566")
    # Pin number verification and objectification
    pin = Pin("00-01", rule=CustomPinNumberRule())

    # Select sending and receiving accounts
    CASH_BIN = DataBase()
    atm_controller = MyAtmController(CASH_BIN)
    src_id, tgt_id = atm_controller.find_accounts(pin)

    # Deduct the amount from the sending account
    # Increasing the amount in the receiving account
    sending_dollar = 30
    atm_controller.withdraw(src_id, sending_dollar)
    atm_controller.deposit(tgt_id, sending_dollar)

    # Print the current balance of the account
    CASH_BIN.print_all_records()


if __name__ == '__main__':
    check_valance()
    send_dollar()
