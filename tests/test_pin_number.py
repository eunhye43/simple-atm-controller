import unittest, re
from string import ascii_letters
from simple_atm_controller.exceptions import InvalidPinNumber, InvalidValidationRule
from simple_atm_controller.pin_number import PinNumber, PinNumberValidationRule


class PinNumberTestCase(unittest.TestCase):

    def test_allocate_pin_number(self):
        pin_number = PinNumber("0000-0001")
        self.assertEqual(pin_number.pin_number, "0000-0001")

    def test_default_exception(self):
        invalid_pin_list = [
            1, .1, ["0000"], ("0000",),
            {"0000"}, {"0000":"0000"},
            # ..., Anything that isn't a string
        ]
        for pin_i in invalid_pin_list:
            try:
                PinNumber(pin_i)
                self.assertTrue(False)
            except InvalidPinNumber:
                pass

    def test_custom_validation_rule(self):

        class CustomPinNumberRule(PinNumberValidationRule):
            def validate(self, pin_number) -> bool:
                # example valid format: 0000, 0001, ...
                return bool(re.search(r"\d{4}", pin_number))

        valid_pin_list = ['{0:04d}'.format(i) for i in range(10000)]
        for valid_pin_i in valid_pin_list:
            PinNumber(valid_pin_i, CustomPinNumberRule())

        for idx in range(len(ascii_letters)):
            try:
                PinNumber(ascii_letters[idx: idx + 4], CustomPinNumberRule())
                self.assertTrue(False)
            except InvalidPinNumber:
                pass

    def test_invalid_validation_rule_exception(self):

        class GoodRule(PinNumberValidationRule):
            def validate(self, pin_number) -> bool:
                return True

        class InvalidReturnRule(PinNumberValidationRule):
            def validate(self, pin_number) -> bool:
                return "True"

        class NotRule:
            pass

        testcase = [
            (GoodRule(), True),
            (InvalidReturnRule(), False),
            (NotRule(), False),
        ]

        for rule, result in testcase:
            try:
                PinNumber("Something", rule)
                self.assertTrue(result)
            except InvalidValidationRule:
                self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
