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


from xerparser.model.classes.fintmpl import FinTmpl


class FinTmpls:

    def __init__(self):
        self.index = 0
        self._FinTmpls = []

    def add(self, params):
        self._FinTmpls.append(FinTmpl(params))

    def get_tsv(self):
        if len(self._FinTmpls) > 0:
            tsv = []
            tsv.append(['%T', 'FINTMPL'])
            tsv.append(["%F", 'fintmpl_id', 'fintmpl_name', 'default_flag'])
            for fin in self._FinTmpls:
                tsv.append(fin.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> FinTmpl:
        obj = list(filter(lambda x: x.fintmpl_id == id, self._FinTmpls))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._FinTmpls)

    def __len__(self):
        return len(self._FinTmpls)

    def __iter__(self):
        return self

    def __next__(self) -> FinTmpl:
        if self.index >= len(self._FinTmpls):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._FinTmpls[idx]
