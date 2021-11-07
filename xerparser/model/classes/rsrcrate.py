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


class ResourceRate:
    obj_list = []

    def __init__(self, params):
        self.rsrc_rate_id = params.get('rsrc_rate_id').strip() if params.get('rsrc_rate_id') else None
        self.rsrc_id = params.get('rsrc_id').strip() if params.get('rsrc_id') else None
        self.max_qty_per_hr = params.get('max_qty_per_hr').strip() if params.get('max_qty_per_hr') else None
        self.cost_per_qty = params.get('cost_per_qty').strip() if params.get('cost_per_qty') else None
        self.start_date = params.get('start_date').strip() if params.get('start_date') else None
        self.shift_period_id = params.get('shift_period_id').strip() if params.get('shift_period_id') else None
        self.cost_per_qty2 = params.get('cost_per_qty2').strip() if params.get('cost_per_qty2') else None
        self.cost_per_qty3 = params.get('cost_per_qty3').strip() if params.get('cost_per_qty3') else None
        self.cost_per_qty4 = params.get('cost_per_qty4').strip() if params.get('cost_per_qty4') else None
        self.cost_per_qty5 = params.get('cost_per_qty5').strip() if params.get('cost_per_qty5') else None
        ResourceRate.obj_list.append(self)

    def get_id(self):
        return self.rsrc_rate_id


    def get_tsv(self):
        tsv =['%R', self.rsrc_rate_id, self.rsrc_id, self.max_qty_per_hr, self.cost_per_qty,
              self.start_date, self.shift_period_id, self.cost_per_qty2, self.cost_per_qty3,
              self.cost_per_qty4, self.cost_per_qty5]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_rate_id == id, cls.obj_list))
        if len(obj) > 0:
            obj = obj[0]
        else:
            None
        return obj

    @classmethod
    def find_by_resource_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_rate_id == id, cls.obj_list))
        if len(obj) > 0:
            obj = obj[0]
        else:
            obj = None
        return obj

    def __repr__(self):
        return self.rsrc_id
