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


from xerparser.model.classes.role import Role


class Roles:

    def __init__(self):
        self.index = 0
        self._roles = []

    def get_tsv(self):
        if len(self._roles) > 0:
            tsv = []
            tsv.append(['%T', 'ROLE'])
            tsv.append(['%F', 'role_id', 'parent_role_id', 'seq_num', 'role_name',
                   'role_short_name', 'pobs_id', 'def_cost_qty_link_flag', 'cost_qty_type',
                   'role_descr', 'last_checksum'])
            for role in self._roles:
                tsv.append(role.get_tsv())
            return tsv
        return []

    def add(self, params):
        self._roles.append(Role(params))

    def find_by_id(self, id) -> Role:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._roles))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._roles)

    def __len__(self):
        return len(self._roles)

    def __iter__(self):
        return iter(self._roles)

    def __next__(self) -> Role:
        if self.index >= len(self._roles):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._roles[idx]
