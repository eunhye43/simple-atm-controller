# simple-atm-controller
This Repo is a simple ATM Controller implemented by using Python3.

The Simple ATM Controller provides the following features .

- PIN Number Validation
- Account Id Validation
- Return all Accounts that PIN Number hasconfirm the balance of the Account 
- Deposit the money to the Account 
- Withdraw money from the Account



# Dependency

- **Python 3.7.1+**



# Test & Sample Code

```bash
$ git clone https://github.com/iml1111/simple-atm-controller
$ cd ~/simple-atm-controller

# Sample Code
$ python3 example.py

# Test Code
$ python3 test.py
```



# Get Started

To use an ATM controller, you need a connection process with the Data Model you are using in your system. For example, I implemented a simple `Database` Class.

(All the codes below can be found at **/tests/data_model.py** and **example.py**)

```python
class DataBase:
    """
    Virtual data model class to run the Test Code
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
        return result[0][2] if result else None

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
```

ATM controller must specify the following approaches for the corresponding Data Model.

- Query that returns the Account ID List that belongs to the entered PIN
- Query that checks the balance of the entered Account
- Query that increases or decreases the balance of the entered Account

If the query is ready, inherit ATM Controller as below and implement the below method by overriding. 

```python
from collections.abc import Iterable
from simple_atm_controller.atm_controller import AtmController


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
```

`self.model` is a variable that holds the entered `data model` when the Controller Class assigns an Instance.

In the method(`find_accounts_query`, `get_valance_query`, `update_valance_query`) ,
you can implement queries in the same way that you used previously to meet each requirement



### Use Controller

If all of the above settings are ready, you can use `Controller`.

First of all, declare `Data Model` and connect it with `Controller` to assign Instance.

```python
CASH_BIN = DataBase()
atm_controller = MyAtmController(CASH_BIN)
```

Assuming that you received the user's card PIN number, create the PIN object as shown below.

```python
from simple_atm_controller.pin import Pin

input_pin = "00-01"
pin = Pin(input_pin)
# print(pin) -> Pin(00-01)
```

If you want to define the logic for verifying the PIN number, 
inherit the `PinValidationRule` class, define the Custom Rule, and then hand it over as a argument when creating the `Pin` object.

```python
from simple_atm_controller.pin import PinValidationRule

class CustomPinNumberRule(PinValidationRule):
    """
    PinNumber Validation Rule
    - Write a rule to verify the pin number
    """
    def validate(self, pin_number) -> bool:
        return bool(re.search(r"\d{2}-\d{2}", pin_number))

pin = Pin(input_pin, rule=CustomPinNumberRule())
```

Pass the `Pin` object to `atm_controller`, check the account list that belongs to it, and select the desired account.

```python
accounts = atm_controller.find_accounts(pin)
selected_account = accounts[0]
# print(accounts)
# [Account(pin_number=00-01, account_id=shino1025), 
#  Account(pin_number=00-01, account_id=shino102566)]
```

By passing the account back as an argument to `atm_controller`, you can use the following functions.

```python
# 잔액 확인
valance = atm_controller.get_valance(selected_account)
# 출금 (status는 출금 성공 여부, msg는 실패시, 실패 사유가 반환됩니다)
status, msg = resuatm_controller.withdraw(selected_account, 30)
# 입금
atm_controller.deposit(selected_account, 30)
```





