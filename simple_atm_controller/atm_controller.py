from collections.abc import Iterable
from abc import ABCMeta, abstractmethod
from .pin_number import PinNumber
from .account_id import AccountId
from .exceptions import (
    AtmControllerException, AtmControllerInputException, AtmControllerQueryException
)


class AtmController(metaclass=ABCMeta):

    def find_accounts(self, pin_number: PinNumber) -> list:
        if not isinstance(pin_number, PinNumber):
            raise AtmControllerInputException("pin_number", "PinNumber")
        results = self.find_accounts_query(pin_number.pin_number)
        if not isinstance(results, Iterable):
            raise AtmControllerQueryException('find_accounts_query', 'Iterable')
        return [AccountId(pin_number, account_id) for account_id in results]

    def get_valance(self, account_id: AccountId) -> int:
        if not isinstance(account_id, AccountId):
            raise AtmControllerInputException("account_id", "AccountId")
        result = self.get_valance_query(*account_id.items)
        if not isinstance(result, int):
            raise AtmControllerQueryException('get_valance_query', 'int')
        return result

    def deposit(self, account_id: AccountId, dollar: int):
        if not isinstance(account_id, AccountId):
            raise AtmControllerInputException("account_id", "AccountId")
        if not (isinstance(dollar, int) and 0 < dollar):
            raise AtmControllerInputException("dollar", "int")
        self.update_valance_query(*account_id.items, dollar)

    def withdraw(self, account_id: AccountId, dollar: int):
        if not isinstance(account_id, AccountId):
            raise AtmControllerInputException("account_id", "AccountId")
        if not (isinstance(dollar, int) and 0 < dollar):
            raise AtmControllerInputException("dollar", "int")
        if dollar <= self.get_valance(account_id):
            self.update_valance_query(*account_id.items, -dollar)
        else:
            raise AtmControllerException("There is insufficient balance in the account")

    @abstractmethod
    def find_accounts_query(self, pin_number) -> Iterable:
        pass

    @abstractmethod
    def get_valance_query(self, pin_number, account_id) -> int:
        pass

    @abstractmethod
    def update_valance_query(self, pin_number, account_id, dollar):
        pass
