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


from xerparser.model.classes.rcatval import RCatVal

class RCatVals:



    def __init__(self):
        self.index = 0
        self._rcatvals = []

    def add(self, params):
        self._rcatvals.append(RCatVal(params))
    
    def get_tsv(self):
        if len(self._rcatvals) > 0:
            tsv = []
            tsv.append(['%T', 'RCATVAL'])
            tsv.append(['%F', 'rsrc_catg_id', 'rsrc_catg_type_id', 'rsrc_catg_short_name',
                        'rsrc_catg_name', 'parent_rsrc_catg_id'])
            for rc in self._rcatvals:
                tsv.append(rc.get_tsv())
            return tsv
        return []
    
    def find_by_id(self, id) -> RCatVal:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rcatvals))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rcatvals)

    def __len__(self):
        return len(self._rcatvals)

    def __iter__(self):
        return self

    def __next__(self) -> RCatVal:
        if self.index >= len(self._rcatvals):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rcatvals[idx]
