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


class RCatType:
    obj_list = []

    def __init__(self, params):
        self.rsrc_catg_type_id = int(params.get('rsrc_catg_type_id').strip()) if params.get('rsrc_catg_type_id') else None
        self.seq_num = params.get('seq_num').strip() if params.get('seq_num') else None
        self.rsrc_catg_short_len = params.get('rsrc_catg_short_len').strip() if params.get('rsrc_catg_short_len') else None
        self.rsrc_catg_type = params.get('rsrc_catg_type').strip() if params.get('rsrc_catg_type') else None
        RCatType.obj_list.append(self)

    def get_tsv(self):
        tsv = ['%R', self.rsrc_catg_type_id,self.seq_num, self.rsrc_catg_short_len,
               self.rsrc_catg_type]
        return tsv

    def get_id(self):
        return self.rsrc_catg_type_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_catg_type_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.rsrc_catg_type