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


from xerparser.model.classes.projcat import ProjCat


class ProjCats:

    def __init__(self):
        self.index = 0
        self._ProjCats = []

    def add(self, params):
        self._ProjCats.append(ProjCat(params))

    def get_tsv(self):
        tsv = []
        if len(self._ProjCats) > 0:
            tsv.append(['%T', 'PROJPCAT'])
            tsv.append(['%F', 'proj_id', 'proj_catg_type_id', 'proj_catg_id'])
            for pcatval in self._ProjCats:
                tsv.append(pcatval.get_tsv())
        return tsv

    # def find_by_id(self, id) -> ProjCat:
    #     obj = list(filter(lambda x: x.proj_catg_id == id, self._ProjCats))
    #     if len(obj) > 0:
    #         return obj[0]
    #     return obj

    @property
    def count(self):
        return len(self._ProjCats)

    def __len__(self):
        return len(self._ProjCats)

    def __iter__(self):
        return self

    def __next__(self) -> ProjCat:
        if self.index >= len(self._ProjCats):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._ProjCats[idx]
