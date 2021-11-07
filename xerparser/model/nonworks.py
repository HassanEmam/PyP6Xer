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


from xerparser.model.classes.nonwork import NonWork


class NonWorks:

    def __init__(self):
        self.index = 0
        self._NonWorks = []

    def add(self, params):
        self._NonWorks.append(NonWork(params))

    def get_tsv(self):
        if len(self._NonWorks) > 0:
            tsv = []
            tsv.append(['%T', 'NONWORK'])
            tsv.append(["%F", 'nonwork_type_id', 'seq_num', 'nonwork_code', 'nonwork_type'])
            for nw in self._NonWorks:
                tsv.append(nw.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> NonWork:
        obj = list(filter(lambda x: x.fintmpl_id == id, self._NonWorks))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._NonWorks)

    def __len__(self):
        return len(self._NonWorks)

    def __iter__(self):
        return self

    def __next__(self) -> NonWork:
        if self.index >= len(self._NonWorks):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._NonWorks[idx]
