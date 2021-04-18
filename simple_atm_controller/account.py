from abc import ABCMeta, abstractmethod
from .exceptions import InvalidAccount, InvalidValidationRule, InvalidPin
from .pin import Pin

class Account:
    """
    The object that manages the account. Receives account_id and verifies the validity.
    """
    def __init__(self, pin: Pin, account_id, rule=None):
        self._pin_number, self._account_id = self._validate(
            pin,
            account_id,
            rule if rule is not None else AccountDefaultRule()
        )

    def _validate(self, pin, account_id, rule):

        if not isinstance(pin, Pin):
            raise InvalidPin(pin)

        if rule.__class__.__bases__[0] is not AccountValidationRule:
            raise InvalidValidationRule('AccountValidationRule')

        validation_result = rule.validate(account_id)
        if not isinstance(validation_result, bool):
            raise InvalidValidationRule('AccountValidationRule')

        if validation_result is True:
            return pin.pin_number, account_id

        raise InvalidAccount(account_id)

    def __repr__(self):
        return f"Account(pin_number={self._pin_number}, " \
               f"account_id={self._account_id})"

    @property
    def pin_number(self):
        return self._pin_number

    @property
    def account_id(self):
        return self._account_id

    @property
    def items(self):
        return self._pin_number, self._account_id


class AccountValidationRule(metaclass=ABCMeta):
    """
    Object to validate account_id.
    You can create an object that can verify the account_id by inheriting the object.
    - The DefaultRule below can be a good example
    """
    @abstractmethod
    def validate(self, account_id) -> bool:
        pass


class AccountDefaultRule(AccountValidationRule):

    def validate(self, account_id) -> bool:
        return isinstance(account_id, str)