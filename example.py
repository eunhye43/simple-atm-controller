"""
Example Code
    # check_valance() : Check the balance for the entered account
    # send_dollar() : Deposit and withdrawal sample code
"""
import re
from collections.abc import Iterable
from simple_atm_controller.pin_number import PinNumber, PinNumberValidationRule
from simple_atm_controller.account_id import AccountId
from simple_atm_controller.atm_controller import AtmController


class MyAtmController(AtmController):
    """
    Overridden ATM Controller
    - You must specify the access method of the data model to the controller
    """

    def find_accounts_query(self, pin_number) -> Iterable:
        return CASH_BIN.find_accounts(pin_number)

    def get_valance_query(self, pin_number, account_id) -> int:
        return CASH_BIN.get_valance(pin_number, account_id)

    def update_valance_query(self, pin_number, account_id, dollar):
        CASH_BIN.update_valance(pin_number, account_id, dollar)


class CustomPinNumberRule(PinNumberValidationRule):
    """
    PinNumber Validation Rule
    - Write a rule to verify the pin number
    """

    def validate(self, pin_number) -> bool:
        return bool(re.search(r"\d{2}-\d{2}", pin_number))


class DataBase:
    """
    Virtual data model class to run the sample code
    """

    def __init__(self):
        self.records = [
            # PIN, AccountId, Valance
            ["00-00", "shin10256", 0],
            ["00-01", "shino1025", 73],
            ["00-01", "shino102566", 23],
            ["00-02", "iml1111", 100_000],
            ["00-03", "imiml", 2312],
        ]

    def find_accounts(self, pin_number):
        """Returns the list of account IDs with the received Pin Number"""
        result =  filter(lambda x: x[0] == pin_number, self.records)
        return [record[1] for record in result]

    def get_valance(self, pin_number, account_id):
        """Return the balance of the account"""
        result = list(filter(
            lambda x: (x[0], x[1]) == (pin_number, account_id),
            self.records
        ))
        if result:
            return result[0][2]
        else:
            raise RuntimeError("DB Error: Can't find the account")

    def update_valance(self, pin_number, account_id, dollar):
        """Modify the balance of the account"""
        for record in self.records:
            if (record[0], record[1]) == (pin_number, account_id):
                record[2] += dollar
                return

    def print_all_records(self):
        """Print all information of current CASH BIN"""
        print("< CASH BIN TOTAL >")
        for item in self.records:
            print("Record(pin=%s, account=%s, valance=%s)" % tuple(item))

# Database for Sample Code
CASH_BIN = DataBase()


def check_valance():
    """Check the balance for the entered account"""
    print("Check Valance Output >>")

    # Input pin number
    input_pin = "00-00"
    # Pin number verification and objectification
    pin_number = PinNumber(input_pin, rule=CustomPinNumberRule())

    # Atm controller call and account selection
    atm_controller = MyAtmController()
    accounts = atm_controller.find_accounts(pin_number)
    selected_account = accounts[0]

    # Print the current balance of the account
    print("%s's Valance: %s" % (
        selected_account,
        atm_controller.get_valance(selected_account)
    ))


def send_dollar():
    """Deposit and withdrawal sample code"""
    print("Send Dollar Output >>")
    # Pin number verification and objectification
    pin_number = PinNumber("00-01", rule=CustomPinNumberRule())

    # Select sending and receiving accounts
    atm_controller = MyAtmController()
    src_id, tgt_id = atm_controller.find_accounts(pin_number)

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
