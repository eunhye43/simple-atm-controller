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
        """Modify the baladonce of the account"""
        for record in self.records:
            if (record[0], record[1]) == (pin_number, account_id):
                record[2] += dollar
                return

    def print_all_records(self):
        """Print all information of current CASH BIN"""
        print("< CASH BIN TOTAL >")
        for item in self.records:
            print("Record(pin=%s, account=%s, valance=%s)" % tuple(item))