from abc import ABCMeta, abstractmethod
from .exceptions import InvalidPinNumber, InvalidValidationRule


class PinNumber:

    def __init__(self, pin_number, rule=None):
        self._pin_number = self._validate(
            pin_number,
            rule if rule is not None else PinNumberDefaultRule()
        )

    def _validate(self, pin_number, rule):
        if rule.__class__.__bases__[0] is not PinNumberValidationRule:
            raise InvalidValidationRule('PinNumberValidationRule')

        validation_result = rule.validate(pin_number)
        if  not isinstance(validation_result, bool):
            raise InvalidValidationRule('PinNumberValidationRule')

        if validation_result is True:
            return pin_number

        raise InvalidPinNumber(pin_number)

    def __repr__(self):
        return f"PinNumber({self._pin_number})"

    @property
    def pin_number(self):
        return self._pin_number


class PinNumberValidationRule(metaclass=ABCMeta):

    @abstractmethod
    def validate(self, pin_number) -> bool:
        pass


class PinNumberDefaultRule(PinNumberValidationRule):

    def validate(self, pin_number ,a=1) -> bool:
        return isinstance(pin_number, str)
