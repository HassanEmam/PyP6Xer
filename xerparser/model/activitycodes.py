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


from xerparser.model.classes.activitycode import ActivityCode


class ActivityCodes:

    def __init__(self):
        self.index = 0
        self._activitycodes = []

    def add(self, params):
        self._activitycodes.append(ActivityCode(params))

    def count(self):
        return len(self._activitycodes)

    def get_tsv(self):
        if len(self._activitycodes) > 0:
            tsv = []
            tsv.append(['%T', 'ACTVCODE'])
            tsv.append(['%F', 'actv_code_id', 'parent_actv_code_id', 'actv_code_type_id',
                        'actv_code_name', 'short_name', 'seq_num', 'color', 'total_assignments'])
            for code in self._activitycodes:
                tsv.append(code.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> ActivityCode:
        obj = list(filter(lambda x: x.actv_code_id == id, self._activitycodes))
        if obj:
            return obj[0]
        return obj

    def find_by_type_id(self, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._activitycodes))
        return obj
    
    def __len__(self):
        return len(self._activitycodes)

    def __iter__(self):
        return self

    def __next__(self) -> ActivityCode:
        if self.index >= len(self._activitycodes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitycodes[idx]
