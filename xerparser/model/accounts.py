# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.


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