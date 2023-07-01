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


from xerparser.model.classes.taskpred import TaskPred
# from xerparser.model.classes.task import Task
from typing import List


class Predecessors:

    def __init__(self):
        self.index=0
        self.task_pred = []

    def find_by_id(self, code_id) -> TaskPred:
        obj = list(filter(lambda x: x.task_pred_id == code_id, self.task_pred))
        if len(obj) > 0:
            obj[0]
        else:
            obj = None
        return obj
    
    def get_tsv(self):
        tsv = []
        if len(self.task_pred) > 0:
            tsv.append(['%T', 'TASKPRED'])
            tsv.append(['%F', 'task_pred_id', 'task_id', 'pred_task_id', 'proj_id', 'pred_proj_id',
               'pred_type', 'lag_hr_cnt', 'comments', 'float_path', 'aref', 'arls'])
            for pred in self.task_pred:
                tsv.append(pred.get_tsv())
        return tsv
        
    def add(self, params):
        pred = TaskPred(params)
        self.task_pred.append(pred)

    @property
    def relations(self) -> List[TaskPred]:
        return self.task_pred

    @property
    def leads(self):
        return list(filter(lambda x: x.lag_hr_cnt < 0 if x.lag_hr_cnt else None, self.task_pred))

    @property
    def finish_to_start(self) -> List[TaskPred]:
        return list(filter(lambda x: x.pred_type == 'PR_FS', self.task_pred))
    
    def get_successors(self, act_id) -> List[TaskPred]:
        succ = list(filter(lambda x: x.pred_task_id == act_id, self.task_pred))
        return succ

    def get_predecessors(self, act_id) -> List[TaskPred]:
        succ = list(filter(lambda x: x.task_id == act_id, self.task_pred))
        return succ

    def count(self):
        return len(self.task_pred)

    def __len__(self):
        return len(self.task_pred)

    def __iter__(self):
        return self

    def __next__(self) -> TaskPred:
        if self.index >= len(self.task_pred):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self.task_pred[idx]

