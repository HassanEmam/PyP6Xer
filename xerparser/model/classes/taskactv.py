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


class TaskActv:
    obj_list = []

    def __init__(self, params, data):
        self.task_id = int(params.get('task_id').strip()) if params.get('task_id') else None
        self.actv_code_type_id = params.get('actv_code_type_id').strip()
        self.actv_code_id = int(params.get('actv_code_id').strip()) if params.get('actv_code_id') else None
        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None
        self.data = data
        TaskActv.obj_list.append(self)

    def get_tsv(self):
        tsv = ['%R', self.task_id, self.actv_code_type_id, self.actv_code_id, self.proj_id]
        return tsv

    def get_id(self):
        return self.task_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return str(self.task_id) + '->' + str(self.actv_code_id)