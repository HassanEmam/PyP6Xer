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


from xerparser.model.classes.taskproc import TaskProc


class TaskProcs:


    def __init__(self):
        self.index = 0
        self._TaskProcs = []

    def add(self, params):
        self._TaskProcs.append(TaskProc(params))

    def get_tsv(self):
        if len(self._TaskProcs) > 0:
            tsv = []
            tsv.append(['%T', 'TASKPROC'])
            tsv.append(["%F", 'proc_id', 'task_id', 'proj_id', 'seq_num', 'proc_name', 'complete_flag',
               'proc_wt', 'complete_pct', 'proc_descr'])
            for taskproc in self._TaskProcs:
                tsv.append(taskproc.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> TaskProc:
        obj = list(filter(lambda x: x.proc_id == id, self._TaskProcs))
        if len(obj) > 0:
            return obj[0]
        return obj

    def find_by_activity_id(self, id):
        objs = list(filter(lambda x: x.task_id == id, self._TaskProcs))
        return objs

    @property
    def count(self):
        return len(self._TaskProcs)

    def __len__(self):
        return len(self._TaskProcs)

    def __iter__(self):
        return self

    def __next__(self) -> TaskProc:
        if self.index >= len(self._TaskProcs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._TaskProcs[idx]
