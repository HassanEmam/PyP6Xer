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


from xerparser.model.classes.schedoption import SchedOption


class SchedOptions:

    def __init__(self):
        self.index = 0
        self._schoptions = []

    def add(self, params):
        self._schoptions.append(SchedOption(params))

    def find_by_id(self, id) -> SchedOption:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._schoptions))
        if len(obj) > 0:
            return obj[0]
        return obj
    
    def get_tsv(self):
        tsv = []
        if len(self._schoptions) > 0:
            tsv.append(['%T', 'SCHEDOPTIONS'])
            tsv.append(['%F', 'schedoptions_id', 'proj_id', 'sched_outer_depend_type', 'sched_open_critical_flag',
               'sched_lag_early_start_flag', 'sched_retained_logic', 'sched_setplantoforecast',
               'sched_float_type', 'sched_calendar_on_relationship_lag', 'sched_use_expect_end_flag',
               'sched_progress_override', 'level_float_thrs_cnt', 'level_outer_assign_flag',
               'level_outer_assign_priority', 'level_over_alloc_pct', 'level_within_float_flag',
               'level_keep_sched_date_flag', 'level_all_rsrc_flag', 'sched_use_project_end_date_for_float',
               'enable_multiple_longest_path_calc', 'limit_multiple_longest_path_calc',
               'max_multiple_longest_path', 'use_total_float_multiple_longest_paths',
               'key_activity_for_multiple_longest_paths', 'LevelPriorityList'])
            for sco in self._schoptions:
                tsv.append(sco.get_tsv())
        return tsv

    @property
    def count(self):
        return len(self._schoptions)

    def __len__(self):
        return len(self._schoptions)

    def __iter__(self):
        return self

    def __next__(self) -> SchedOption:
        if self.index >= len(self._schoptions):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._schoptions[idx]
