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


class Role:
    obj_list = []

    def __init__(self, params):
        self.role_id = int(params.get('role_id')) if params.get('role_id') else None
        self.parent_role_id = int(params.get('parent_role_id')) if params.get('parent_role_id') else None
        self.seq_num = int(params.get('seq_num')) if params.get('seq_num') else None
        self.role_name = params.get('role_name') if params.get('role_name') else None
        self.role_short_name = params.get('role_short_name') if params.get('role_short_name') else None
        self.pobs_id = params.get('pobs_id') if params.get('pobs_id') else None
        self.def_cost_qty_link_flag = params.get('def_cost_qty_link_flag') if params.get('def_cost_qty_link_flag') else None
        self.cost_qty_type = params.get('cost_qty_type') if params.get('cost_qty_type') else None
        self.role_descr = params.get('role_descr') if params.get('role_descr') else None
        self.last_checksum = params.get('role_descr') if params.get('role_descr') else None

        Role.obj_list.append(self)

    def get_tsv(self):
        tsv = ['%R', self.role_id, self.parent_role_id, self.seq_num, self.role_name,
               self.role_short_name, self.pobs_id, self.def_cost_qty_link_flag, self.cost_qty_type,
               self.role_descr, self.last_checksum]
        return tsv

    def __repr__(self):
        return self.role_name
