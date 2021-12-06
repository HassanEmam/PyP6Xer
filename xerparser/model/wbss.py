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


from xerparser.model.classes.wbs import WBS
from typing import List


class WBSs:

    def __init__(self, data=None):
        self.index = 0
        self._wbss = []
        self.data = data

    def add(self, params, data):
        wbs = WBS(params, data)
        self._wbss.append(wbs)
    
    def get_tsv(self):
        tsv = []
        if len(self._wbss) > 0:
            tsv.append(['%T', 'PROJWBS'])
            tsv.append(['%F', 'wbs_id', 'proj_id', 'obs_id', 'seq_num', 'est_wt',
               'proj_node_flag', 'sum_data_flag', 'status_code', 'wbs_short_name',
               'wbs_name', 'phase_id', 'parent_wbs_id', 'ev_user_pct', 'ev_etc_user_value',
               'orig_cost', 'indep_remain_total_cost', 'ann_dscnt_rate_pct', 'dscnt_period_type',
               'indep_remain_work_qty', 'anticip_start_date', 'anticip_end_date', 'ev_compute_type',
               'ev_etc_compute_type', 'guid', 'tmpl_guid', 'plan_open_state'])
            for wb in self._wbss:
                tsv.append(wb.get_tsv())
        return tsv
    
    def get_by_project(self, id) -> List[WBS]:
        return list(filter(lambda x: x.proj_id == id, self._wbss))

    def __iter__(self):
        return self

    def __next__(self) -> WBS:
        if self.index >= len(self._wbss):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._wbss[idx]
