from abc import ABCMeta, abstractmethod
from .exceptions import InvalidAccountId, InvalidValidationRule, InvalidPinNumber
from .pin_number import PinNumber

class AccountId:

    def __init__(self, pin_number: PinNumber, account_id, rule=None):
        self._pin_number, self._account_id = self._validate(
            pin_number,
            account_id,
            rule if rule is not None else AccountIdDefaultRule()
        )

    def _validate(self, pin_number, account_id, rule):

        if not isinstance(pin_number, PinNumber):
            raise InvalidPinNumber(pin_number)

        if rule.__class__.__bases__[0] is not AccountIdValidationRule:
            raise InvalidValidationRule('AccountIdValidationRule')

        validation_result = rule.validate(account_id)
        if not isinstance(validation_result, bool):
            raise InvalidValidationRule('AccountIdValidationRule')

        if validation_result is True:
            return pin_number.pin_number, account_id

        raise InvalidAccountId(account_id)

    def __repr__(self):
        return f"AccountId(pin_number={self._pin_number}, " \
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


class AccountIdValidationRule(metaclass=ABCMeta):

    @abstractmethod
    def validate(self, account_id) -> bool:
        pass


class AccountIdDefaultRule(AccountIdValidationRule):

    def validate(self, account_id) -> bool:
        return isinstance(account_id, str)