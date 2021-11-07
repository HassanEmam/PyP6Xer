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


from xerparser.model.classes.udfvalue import UDFValue


class UDFValues:

    def __init__(self):
        self.index = 0
        self._udfvalues = []

    def add(self, params):
        self._udfvalues.append(UDFValue(params))

    def get_tsv(self):
        if len(self._udfvalues) > 0:
            tsv = []
            tsv.append(['%T', 'UDFVALUE'])
            tsv.append(["%F", 'udf_type_id', 'fk_id', 'proj_id', 'udf_date', 'udf_number', 'udf_text',
               'udf_code_id'])
            for udfval in self._udfvalues:
                tsv.append(udfval.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> UDFValue:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._udfvalues))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._udfvalues)

    def __len__(self):
        return len(self._udfvalues)

    def __iter__(self):
        return self

    def __next__(self) -> UDFValue:
        if self.index >= len(self._udfvalues):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._udfvalues[idx]
