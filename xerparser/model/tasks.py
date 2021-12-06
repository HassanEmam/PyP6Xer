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


from xerparser.model.classes.task import Task
from xerparser.model.classes.taskpred import TaskPred
from xerparser.model.classes.taskactv import TaskActv
from xerparser.model.predecessors import Predecessors
from typing import List


class Tasks:
    """
    This class is a collection of tasks that controls functionalities to search, add, update and delete tasks
    """
    

    def __init__(self):
        self.index = 0
        self._tasks = []

    def add(self, params, data):
        task = Task(params, data)
        self._tasks.append(task)

    @property
    def activities(self) -> List[Task]:
        return self._tasks

    @property
    def count(self):
        return len(self._tasks)

    @property
    def has_no_successor(self):
        objs = list(filter(lambda x: x.task_id not in [z.pred_task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    @property
    def has_no_predecessor(self):
        objs = list(filter(lambda x: x.task_id not in [z.task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    def __len__(self):
        return len(self._tasks)

    def __repr__(self):
        return [x.task_code for x in self._tasks]

    def __str__(self):
        return str([str(x.task_code) for x in self._tasks])

    @property
    def constraints(self):
        lst = [x.constraints if x.constraints is not None else None for x in self._tasks]
        # print(lst)
        return list(filter(lambda x: x is not None, lst))

    def find_by_id(self, id):
        obj = list(filter(lambda x: x.task_id == id, self._tasks))
        if len(obj) > 0:
            return obj[0]
        return obj

    def find_by_code(self, code):
        obj = list(filter(lambda x: x.task_code == code, self._tasks))
        if len(obj) > 0:
            return obj[0]
        return obj

    def duration_greater_than(self, duration):
        obj = list(filter(lambda x: x.target_drtn_hr_cnt > duration * float(self.calendar.day_hr_cnt), self._tasks))
        if obj:
            return obj
        return obj

    def float_less_than(self, Tfloat):
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        obj = list(filter(lambda x: x.total_float_hr_cnt < Tfloat * float(x.calendar.day_hr_cnt), objs))
        if obj:
            return obj
        return obj

    def float_greater_than(self, Tfloat):
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        obj = list(filter(lambda x: x.total_float_hr_cnt > Tfloat * float(x.calendar.day_hr_cnt), objs))
        if obj:
            return obj
        return obj

    def float_within_range(self, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        if float1 < float2:
            obj = list(filter(lambda x: x.total_float_hr_cnt >= float1 * float(x.calendar.day_hr_cnt) and x.total_float_hr_cnt <= float2 * float(x.calendar.day_hr_cnt), objs))
            if obj:
                return obj
        return obj

    def float_within_range_exclusive(self, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", self._tasks))
        if float1 < float2:
            obj = list(filter(lambda x: x.total_float_hr_cnt > float1 * float(x.calendar.day_hr_cnt) and x.total_float_hr_cnt < float2 * float(x.calendar.day_hr_cnt), objs))
            if obj:
                return obj
        return obj

    def activities_by_status(self, status):
        objs = list(filter(lambda x: x.status_code == status, self._tasks))
        return objs

    def activities_by_wbs_id(self, id):
        objs = list(filter(lambda x: x.wbs_id == id, self._tasks))
        return objs

    def activities_by_activity_code_id(self, id):
        objs = list(filter(lambda x: x.actv_code_id == id, TaskActv.obj_list))
        activities = []
        for obj in objs:
            activities.append(self.find_by_id(obj.task_id))
        return activities

    def no_predecessors(self):
        objs = list(filter(lambda x: x.task_id not in [z.task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    def no_successors(self):
        objs = list(filter(lambda x: x.task_id not in [z.pred_task_id for z in TaskPred.obj_list], self._tasks))
        return objs

    def activities_with_hard_contratints(self):
        obj = list(filter(lambda x: x.cstr_type == "CS_MEO" or x.cstr_type == "CS_MSO", self._tasks))
        return obj

    def activities_by_type(self, type):
        obj = list(filter(lambda x: x.cstr_type == type, self._tasks))
        return obj
    
    def get_tsv(self):
        tsv = []
        if len(self._tasks) > 0:
            tsv.append(['%T', 'TASK'])
            tsv.append(['%F', 'task_id', 'proj_id', 'wbs_id', 'clndr_id', 'phys_complete_pct', 'rev_fdbk_flag',
               'est_wt', 'lock_plan_flag', 'auto_compute_act_flag', 'complete_pct_type', 'task_type',
               'duration_type', 'status_code', 'task_code', 'task_name', 'rsrc_id',
               'total_float_hr_cnt', 'free_float_hr_cnt', 'remain_drtn_hr_cnt', 'act_work_qty',
               'remain_work_qty', 'target_work_qty', 'target_drtn_hr_cnt', 'target_equip_qty',
               'act_equip_qty', 'remain_equip_qty', 'cstr_date', 'act_start_date', 'act_end_date',
               'late_start_date', 'late_end_date', 'expect_end_date', 'early_start_date',
               'early_end_date', 'restart_date', 'reend_date', 'target_start_date', 'target_end_date',
               'rem_late_start_date', 'rem_late_end_date', 'cstr_type', 'priority_type', 'suspend_date',
               'resume_date', 'float_path', 'float_path_order', 'guid', 'tmpl_guid', 'cstr_date2',
               'cstr_type2', 'driving_path_flag', 'act_this_per_work_qty', 'act_this_per_equip_qty',
               'external_early_start_date', 'external_late_end_date', 'create_date', 'update_date',
               'create_user', 'update_user', 'location_id'])
            for task in self._tasks:
                tsv.append(task.get_tsv())
        return tsv

    def get_by_project(self, id):
        obj = list(filter(lambda x: x.proj_id == id, self._tasks))
        return obj

    def __iter__(self):
        return self

    def __next__(self) -> Task:
        if self.index >= len(self._tasks):
            raise StopIteration
        idx = self.index
        self.index +=1
        return self._tasks[idx]
