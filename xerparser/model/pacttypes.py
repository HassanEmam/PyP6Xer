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


from xerparser.model.classes.pcattype import PCatType


class PCatTypes:

    def __init__(self):
        self.index = 0
        self._pcattypes = []

    def add(self, params):
        self._pcattypes.append(PCatType(params))

    def find_by_id(self, id) -> PCatType:
        obj = list(filter(lambda x: x.proj_catg_type_id == id, self._pcattypes))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        if len(self._pcattypes) > 0:
            tsv = []
            tsv.append(['%T', 'PCATTYPE'])
            tsv.append(['%F', 'proj_catg_type_id', 'seq_num', 'proj_catg_short_len',
               'proj_catg_type', 'export_flag'])
            for acttyp in self._pcattypes:
                tsv.append(acttyp.get_tsv())
            return tsv
        return []

    def count(self):
        return len(self._pcattypes)

    def __len__(self):
        return len(self._pcattypes)

    def __iter__(self):
        return self

    def __next__(self) -> PCatType:
        if self.index >= len(self._pcattypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._pcattypes[idx]