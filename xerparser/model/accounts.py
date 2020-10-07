from xerparser.model.classes.account import Account

class Accounts:
    _accounts = []
    def __init__(self):
        self.index = 0

    def add_account(self, params):
        self._accounts.append(Account(params))

    @staticmethod
    def count():
        return len(Accounts.task_pred)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.task_pred):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self.task_pred[idx]