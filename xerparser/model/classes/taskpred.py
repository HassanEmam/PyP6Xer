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


class TaskPred:

    obj_list = []

    def __init__(self, params):
        tpi = params.get('task_pred_id').strip() if params.get('task_pred_id') else None
        self.task_pred_id = int(tpi) if tpi is not None and tpi.isdigit() else tpi
        self.task_id = int(params.get('task_id')) if params.get('task_id') else None
        self.pred_task_id = int(params.get('pred_task_id')) if params.get('pred_task_id') else None
        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None
        self.pred_proj_id = int(params.get('pred_proj_id').strip()) if params.get('pred_proj_id') else None
        self.pred_type = params.get('pred_type').strip() if params.get('pred_type') else None
        self.lag_hr_cnt = float(params.get('lag_hr_cnt').strip()) if params.get('lag_hr_cnt') else None
        self.float_path = params.get('float_path').strip() if params.get('float_path') else None
        self.aref = params.get('aref').strip() if params.get('aref') else None
        self.arls = params.get('arls').strip() if params.get('arls') else None
        self.comments = params.get('comments').strip() if params.get('comments') else None
        TaskPred.obj_list.append(self)

    @classmethod
    def create(cls, task_id, pred_task_id, pred_type="PR_FS", lag_hr_cnt=None,
               proj_id=None, pred_proj_id=None, comments=None, task_pred_id=None):
        """Build a new TaskPred from typed values (editing API).

        Values are normalized the same way the reader normalizes parsed
        rows, so a created record writes back identically to a read one.
        """
        params = {
            'task_pred_id': None if task_pred_id is None else str(task_pred_id),
            'task_id': None if task_id is None else str(int(task_id)),
            'pred_task_id': None if pred_task_id is None else str(int(pred_task_id)),
            'proj_id': None if proj_id is None else str(int(proj_id)),
            'pred_proj_id': None if pred_proj_id is None else str(int(pred_proj_id)),
            'pred_type': pred_type,
            'lag_hr_cnt': None if lag_hr_cnt is None else str(float(lag_hr_cnt)),
            'comments': comments,
            'float_path': None,
            'aref': None,
            'arls': None,
        }
        return cls(params)

    def get_id(self):
        return self.task_pred_id

    def get_tsv(self):
        tsv = ['%R', self.task_pred_id, self.task_id, self.pred_task_id, self.proj_id, self.pred_proj_id,
               self.pred_type, self.lag_hr_cnt, self.comments, self.float_path, self.aref, self.arls]
        return tsv
    
    def __repr__(self):
        return str(self.pred_task_id) + '- ' + self.pred_type + ' ->' + str(self.task_id) + ' lag: ' + str(self.lag_hr_cnt)