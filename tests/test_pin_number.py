import unittest, re
from string import ascii_letters
from simple_atm_controller.exceptions import InvalidPin, InvalidValidationRule
from simple_atm_controller.pin import Pin, PinValidationRule


class PinNumberTestCase(unittest.TestCase):
    # 핀넘버가 포맷에 맞는지 테스트(s)
    def test_allocate_pin_number(self):
        pin_number = Pin("0000-0001")
        self.assertEqual(pin_number.pin_number, "0000-0001")
    # 잘못된 형태의 핀넘버 유형들이 들어왔을 때 테스트(f)
    def test_default_exception(self):
        invalid_pin_list = [
            1, .1, ["0000"], ("0000",),
            {"0000"}, {"0000":"0000"},
            # ..., Anything that isn't a string
        ]
        for pin_i in invalid_pin_list:
            try:
                Pin(pin_i) # 핀 객체에 넣고 포맷 확인
                self.assertTrue(False) # false가 들어가면 에러가뜨니까
            except InvalidPin: # 에러처리
                pass
  
    def test_custom_validation_rule(self):
        # 핀넘버 cumtom했을때 / 숫자 4자리인지 확인하는 테스트
        class CustomPinNumberRule(PinValidationRule):
            def validate(self, pin_number) -> bool:
                # example valid format: 0000, 0001, ...
                return bool(re.search(r"\d{4}", pin_number))
        # 0부터 10000까지 4자리씩 뽑아냄 -> valid_pin_list에 넣음
        valid_pin_list = ['{0:04d}'.format(i) for i in range(10000)]
        for valid_pin_i in valid_pin_list:#10000부터 i 하나씩 뽑음(4자리)
            Pin(valid_pin_i, CustomPinNumberRule()) # pin객체 생성
   
        for idx in range(len(ascii_letters)): # 0부터 52까지 돌리면서 ids추출(근데 왜 ascii_letters일까)
            try:
                Pin(ascii_letters[idx: idx + 4], CustomPinNumberRule()) #4자리 숫자가 pin 포맷에 맞는지 확인
                self.assertTrue(False) # True확인하는 함수에 False를 넣었으니 에러가 나겠지
            except InvalidPin: # except구문으로와서 InvalidPin 에러 발생
                pass

    def test_invalid_validation_rule_exception(self):
        # pin_number format 유효한지 확인(f)
        class GoodRule(PinValidationRule):
            def validate(self, pin_number) -> bool:
                return True
        # GoodRule과의 차이? -> 왜 반환값이 str ?
        class InvalidReturnRule(PinValidationRule):
            def validate(self, pin_number) -> bool:
                return "True"
        # NotRule ?
        class NotRule:
            pass

        testcase = [
            (GoodRule(), True),
            (InvalidReturnRule(), False),
            (NotRule(), False),
        ]
        # ?
        for rule, expect in testcase:
            try:
                Pin("Something", rule)
                self.assertTrue(expect)
            except InvalidValidationRule:
                self.assertFalse(expect)


if __name__ == '__main__':
    unittest.main()