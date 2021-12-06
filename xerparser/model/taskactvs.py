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


from xerparser.model.classes.taskactv import TaskActv


class TaskActvs:

    def __init__(self):
        self.index = 0
        self._taskactvs = []

    def add(self, params, data):
        self._taskactvs.append(TaskActv(params, data))
    
    def get_tsv(self):
        tsv = []
        if len(self._taskactvs) > 0:
            tsv.append(['%T', 'TASKACTV'])
            tsv.append(['%F', 'task_id', 'actv_code_type_id', 'actv_code_id', 'proj_id'])
            for taskact in self._taskactvs:
                tsv.append(taskact.get_tsv())
        return tsv
    
    def find_by_code_id(self, id) -> TaskActv:
        obj = list(filter(lambda x: x.actv_code_id == id, self._taskactvs))
        if len(obj) > 0:
            return obj
        return obj

    def find_by_activity_id(self, id) -> TaskActv:
        obj = list(filter(lambda x: x.task_id == id, self._taskactvs))
        if len(obj) > 0:
            return obj
        return obj

    def count(self):
        return len(self._taskactvs)

    def __len__(self):
        return len(self._taskactvs)

    def __iter__(self):
        return self

    def __next__(self) -> TaskActv:
        if self.index >= len(self._taskactvs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._taskactvs[idx]