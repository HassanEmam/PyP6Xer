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
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html.


from xerparser.model.classes.rsrc_curv import RsrcCurv


class RsrcCurves:
    """Collection of RSRCCURV resource-curve definition rows."""

    def __init__(self):
        self.index = 0
        self._rsrc_curvs = []

    def add(self, params):
        self._rsrc_curvs.append(RsrcCurv(params))

    def find_by_id(self, id):
        obj = list(filter(lambda x: x.curv_id == id, self._rsrc_curvs))
        if len(obj) > 0:
            return obj[0]
        return None

    def get_tsv(self):
        if not self._rsrc_curvs:
            return []
        tsv = []
        tsv.append(['%T', 'RSRCCURV'])
        tsv.append(['%F', 'curv_data', 'curv_id', 'curv_name', 'default_flag'])
        for curv in self._rsrc_curvs:
            tsv.append(curv.get_tsv())
        return tsv

    @property
    def count(self):
        return len(self._rsrc_curvs)

    def __len__(self):
        return len(self._rsrc_curvs)

    def __iter__(self):
        return iter(self._rsrc_curvs)

    def __next__(self) -> RsrcCurv:
        if self.index >= len(self._rsrc_curvs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrc_curvs[idx]
