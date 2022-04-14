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

import locale

class RoleRate:
    obj_list = []

    def __init__(self, params):
        self.role_rate_id = int(params.get('role_rate_id').strip()) if params.get('role_rate_id') else None
        self.role_id = int(params.get('role_id').strip()) if params.get('role_id') else None
        self.cost_per_qty = locale.atof(params.get('cost_per_qty').strip()) if params.get('cost_per_qty') else None
        self.cost_per_qty2 = locale.atof(params.get('cost_per_qty2').strip())if params.get('cost_per_qty2') else None
        self.cost_per_qty3 = locale.atof(params.get('cost_per_qty3').strip()) if params.get('cost_per_qty3') else None
        self.cost_per_qty4 = locale.atof(params.get('cost_per_qty4').strip()) if params.get('cost_per_qty4') else None
        self.cost_per_qty5 = locale.atof(params.get('cost_per_qty5').strip()) if params.get('cost_per_qty5') else None

        RoleRate.obj_list.append(self)

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.role_rate_id == id, cls.obj_list))[0]
        return obj

    def get_tsv(self):
        tsv = ['%R', self.role_rate_id, self.role_id, self.cost_per_qty, self.cost_per_qty2,
               self.cost_per_qty3, self.cost_per_qty4, self.cost_per_qty5]
        return tsv

    @classmethod
    def find_by_role_id(cls, id):
        obj = list(filter(lambda x: x.role_id == id, cls.obj_list))
        if len(obj) > 0:
            obj = obj[0]
        else:
            obj = None
        return obj

    def __repr__(self):
        return str(self.role_rate_id)
