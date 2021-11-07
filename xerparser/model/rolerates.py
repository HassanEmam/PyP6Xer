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


from xerparser.model.classes.rolerate import RoleRate


class RoleRates:

    def __init__(self):
        self.index = 0
        self._rolerates = []

    def get_tsv(self):
        tsv = []
        if len(self._rolerates) > 0:
            tsv.append(['%T', 'ROLERATE'])
            tsv.append(['%F', 'role_rate_id', 'role_id', 'cost_per_qty', 'cost_per_qty2',
                   'cost_per_qty3', 'cost_per_qty4', 'cost_per_qty5'])
            for rr in self._rolerates:
                tsv.append(rr.get_tsv())
        return tsv

    def add(self, params):
        self._rolerates.append(RoleRate(params))
        self._rolerates = []

    def find_by_id(self, id) -> RoleRate:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rolerates))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rolerates)

    def __len__(self):
        return len(self._rolerates)

    def __iter__(self):
        return self

    def __next__(self) -> RoleRate:
        if self.index >= len(self._rolerates):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rolerates[idx]