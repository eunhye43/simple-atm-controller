from collections.abc import Iterable
from abc import ABCMeta, abstractmethod
from .pin import Pin
from .account import Account
from .exceptions import (
    AtmControllerException, AtmControllerInputException, AtmControllerQueryException
)


class AtmController(metaclass=ABCMeta):
    """
    It is a controller that performs the functions of ATM.
    The controller supports the following functions
        - Receive pin and search for registered account.(find_accounts)
        - Receives an account and returns the balance of the account.(get_valance)
        - Receives an account and (withdraw) or (deposit) dollars from that account.

    In order to use the controller,
    you need to define the access method to the cash bin to the controller.
    The controller needs to know the following query to access the cash bin.
        - Query to search account through pin
        - Query to check the balance of the account
        - Query to change the balance of that account
    """

    def __init__(self, model=None):
        self.model = model

    def find_accounts(self, pin: Pin) -> list:
        if not isinstance(pin, Pin):
            raise AtmControllerInputException("pin", "Pin")
        results = self.find_accounts_query(pin.pin_number)
        if not isinstance(results, Iterable):
            raise AtmControllerQueryException('find_accounts_query', 'Iterable')
        return [Account(pin, account_id) for account_id in results]

    def get_valance(self, account: Account) -> int:
        if not isinstance(account, Account):
            raise AtmControllerInputException("account", "Account")
        result = self.get_valance_query(*account.items)
        if not (isinstance(result, int) or result is None):
            raise AtmControllerQueryException('get_valance_query', 'int')
        return result

    def deposit(self, account: Account, dollar: int):
        if not isinstance(account, Account):
            raise AtmControllerInputException("account", "Account")
        if not isinstance(dollar, int):
            raise AtmControllerInputException("dollar", "int")
        if dollar < 0:
            raise AtmControllerException("Negative values cannot be entered for 'dollar'")
        self.update_valance_query(*account.items, dollar)

    def withdraw(self, account: Account, dollar: int):
        if not isinstance(account, Account):
            raise AtmControllerInputException("account_id", "AccountId")
        if not isinstance(dollar, int):
            raise AtmControllerInputException("dollar", "int")
        if dollar < 0:
            raise AtmControllerException("Negative values cannot be entered for 'dollar'")
        if dollar <= self.get_valance(account):
            self.update_valance_query(*account.items, -dollar)
            return True, "success"
        else:
            return False, "insufficient balance"

    @abstractmethod
    def find_accounts_query(self, pin_number) -> Iterable:
        pass

    @abstractmethod
    def get_valance_query(self, pin_number, account_id) -> int:
        pass

    @abstractmethod
    def update_valance_query(self, pin_number, account_id, dollar):
        pass
