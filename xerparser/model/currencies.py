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


from xerparser.model.classes.currency import Currency

class Currencies:



    def __init__(self):
        self.index = 0
        self._currencies = []

    def add(self, params):
        self._currencies.append(Currency(params))

    def find_by_id(self, id) -> Currency:
        obj = list(filter(lambda x: x.curr_id == id, self._currencies))
        if len(obj) > 0:
            return obj[0]
        return obj
    
    def get_tsv(self):
        if len(self._currencies) > 0:
            tsv = []
            tsv.append(['%T', 'CURRTYPE'])
            tsv.append(['%F', 'curr_id', 'decimal_digit_cnt', 'curr_symbol', 'decimal_symbol',
                   'digit_group_symbol', 'pos_curr_fmt_type', 'neg_curr_fmt_type', 'curr_type', 'curr_short_name',
                   'group_digit_cnt', 'base_exch_rate'])
            for cur in self._currencies:
                tsv.append(cur.get_tsv())
            return tsv
        return []

    @property
    def count(self):
        return len(self._currencies)

    def __len__(self):
        return len(self._currencies)

    def __iter__(self):
        return self

    def __next__(self) -> Currency:
        if self.index >= len(self._currencies):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._currencies[idx]