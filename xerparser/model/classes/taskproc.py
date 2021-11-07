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


class TaskProc:

    def __init__(self, params):

        self.complete_flag = params.get('complete_flag').strip() if params.get('complete_flag') else None
        self.complete_pct = params.get('complete_pct').strip() if params.get('complete_pct') else None
        self.proc_descr = params.get('proc_descr').strip() if params.get('proc_descr') else None
        self.proc_id = params.get('proc_id').strip() if params.get('proc_id') else None
        self.proc_name = params.get('proc_name').strip() if params.get('proc_name') else None
        self.proc_wt = params.get('proc_wt').strip() if params.get('proc_wt') else None
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.seq_num = params.get('seq_num').strip() if params.get('seq_num') else None
        self.task_id = params.get('task_id').strip() if params.get('task_id') else None


    def get_id(self):
        return self.proc_id

    def get_tsv(self):
        tsv = ["%R", self.proc_id, self.task_id, self.proj_id, self.seq_num, self.proc_name, self.complete_flag,
               self.proc_wt, self.complete_pct, self.proc_descr ]
        return tsv


    def __repr__(self):
        return self.proc_id + '->' + self.task_id