from xerparser.model.classes.account import Account

class Accounts:

    def __init__(self):
        self._accounts = []
        self.index = 0

    def add(self, params):
        self._accounts.append(Account(params))

    def get_tsv(self):
        if len(self._accounts) > 0:
            tsv = list()
            tsv.append(["%T", "ACCOUNT"])
            tsv.append(["%F", "acct_id", "parent_acct_id", "acct_seq_num", "acct_name", "acct_short_name",
                        "acct_descr"])
            for account in self._accounts:
                tsv.append(account.get_tsv())
            return tsv
        return []

    def count(self):
        return len(self._accounts)

    def __iter__(self):
        return self

    def __next__(self) -> Account:
        if self.index >= len(self._accounts):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._accounts[idx]