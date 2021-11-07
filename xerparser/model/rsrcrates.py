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


from xerparser.model.classes.rsrcrate import ResourceRate

class ResourceRates:

    def __init__(self):
        self.index = 0
        self._rsrcrates = []

    def add(self, params):
        self._rsrcrates.append(ResourceRate(params))

    def find_by_id(self, id) -> ResourceRate:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rsrcrates))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        tsv = []
        if len(self._rsrcrates) > 0:
            tsv.append(['%T', 'RSRCRATE'])
            tsv.append(['%F', 'rsrc_rate_id', 'rsrc_id', 'max_qty_per_hr', 'cost_per_qty',
              'start_date', 'shift_period_id', 'cost_per_qty2', 'cost_per_qty3',
              'cost_per_qty4', 'cost_per_qty5'])
            for rr in self._rsrcrates:
                tsv.append(rr.get_tsv())
        return tsv

    @property
    def count(self):
        return len(self._rsrcrates)

    def __len__(self):
        return len(self._rsrcrates)

    def __iter__(self):
        return self

    def __next__(self) -> ResourceRate:
        if self.index >= len(self._rsrcrates):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrcrates[idx]
