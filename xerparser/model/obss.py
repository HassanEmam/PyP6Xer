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


from xerparser.model.classes.obs import OBS

class OBSs:



    def __init__(self):
        self.index = 0
        self._obss = []

    def add(self, params):
        self._obss.append(OBS(params))

    def find_by_id(self, id) -> OBS:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._obss))
        if len(obj) > 0:
            return obj[0]
        return obj
    
    def get_tsv(self):
        if len(self._obss) > 0:
            tsv = []
            tsv.append(['%T', 'OBS'])
            tsv.append(['%F', 'obs_id', 'parent_obs_id', 'guid', 'seq_num',
                        'obs_name', 'obs_descr'])
            for obs in self._obss:
                tsv.append(obs.get_tsv())
            return tsv
        return []
    
    @property
    def count(self):
        return len(self._obss)

    def __len__(self):
        return len(self._obss)

    def __iter__(self):
        return self

    def __next__(self) -> OBS:
        if self.index >= len(self._obss):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._obss[idx]