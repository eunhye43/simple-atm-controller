from abc import ABCMeta, abstractmethod
from .exceptions import InvalidPin, InvalidValidationRule


class Pin:
    """
    It is an object that receives Pin Number, verifies and manages it.
    """
    def __init__(self, pin_number, rule=None):
        self._pin_number = self._validate(
            pin_number,
            rule if rule is not None else PinDefaultRule()
        )

    def _validate(self, pin_number, rule):
        if rule.__class__.__bases__[0] is not PinValidationRule:
            raise InvalidValidationRule('PinValidationRule')

        validation_result = rule.validate(pin_number)
        if  not isinstance(validation_result, bool):
            raise InvalidValidationRule('PinValidationRule')

        if validation_result is True:
            return pin_number

        raise InvalidPin(pin_number)

    def __repr__(self):
        return f"Pin({self._pin_number})"

    @property
    def pin_number(self):
        return self._pin_number


class PinValidationRule(metaclass=ABCMeta):
    """
     Object to validate pin_number.
     You can create an object that can verify the pin_number by inheriting the object.
     - The DefaultRule below can be a good example
     """
    @abstractmethod
    def validate(self, pin_number) -> bool:
        pass


class PinDefaultRule(PinValidationRule):

    def validate(self, pin_number ,a=1) -> bool:
        return isinstance(pin_number, str)
