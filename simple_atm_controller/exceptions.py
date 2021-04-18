
class InvalidPin(Exception):

    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"Invalid Pin Number Format/Type: {self._param}"


class InvalidValidationRule(Exception):

    def __init__(self, rule_type):
        self._rule_type = rule_type

    def __str__(self):
        return f"Invalid Valudation Rule. "\
               f"The rule must be '{self._rule_type}'. "\
               f"Then, rule valdiation function must return to True/False."


class InvalidAccount(Exception):

    def __init__(self, param):
        self._param = param

    def __str__(self):
        return f"Invalid AccountId Format/Type: {self._param}"


class AtmControllerException(Exception):

    def __init__(self, param):
        self._param = param

    def __str__(self):
        return self._param


class AtmControllerInputException(Exception):

    def __init__(self, param, valid_type):
        self._param = param
        self._valid_type = valid_type

    def __str__(self):
        return f"Invalid '{self._param}' param. " \
               f"This param must '{self._valid_type}' object."


class AtmControllerQueryException(Exception):

    def __init__(self, param, valid_type):
        self._param = param
        self._valid_type = valid_type

    def __str__(self):
        return f"Invalid '{self._param}' methods. " \
               f"This function must return to '{self._valid_type}' object."