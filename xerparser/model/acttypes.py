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


from xerparser.model.classes.acttype import ActType

class ActTypes:



    def __init__(self):
        self.index = 0
        self._activitytypes = []

    def add(self, params):
        self._activitytypes.append(ActType(params))

    def find_by_id(self, id) -> ActType:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._activitytypes))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        if len(self._activitytypes) > 0:
            tsv = []
            tsv.append(['%T', 'ACTVTYPE'])
            tsv.append(['%F', 'actv_code_type_id', 'actv_short_len', 'seq_num',
                        'actv_code_type', 'proj_id', 'wbs_id', 'actv_code_type_scope'])
            for acttyp in self._activitytypes:
                tsv.append(acttyp.get_tsv())
            return tsv
        return []

    def count(self):
        return len(self._activitytypes)

    def __len__(self):
        return len(self._activitytypes)

    def __iter__(self):
        return self

    def __next__(self) -> ActType:
        if self.index >= len(self._activitytypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitytypes[idx]