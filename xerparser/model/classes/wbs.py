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


from xerparser.model.tasks import Tasks
from xerparser.model.classes.task import Task

class WBS:
    obj_list = []

    def __init__(self, params, data=None):
        def _s(key):
            """Strip a string column; missing columns (older schemas) yield None."""
            v = params.get(key)
            return v.strip() if isinstance(v, str) else None
        self.wbs_id = int(params.get('wbs_id').strip()) if params.get('wbs_id') else None
        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None
        self.obs_id = _s('obs_id')
        self.seq_num = _s('seq_num')
        self.est_wt = params.get('est_wt')
        self.proj_node_flag = _s('proj_node_flag')
        self.sum_data_flag = _s('sum_data_flag')
        self.status_code = _s('status_code')
        self.wbs_short_name = _s('wbs_short_name')
        self.wbs_name = _s('wbs_name')
        self.phase_id = _s('phase_id')
        self.parent_wbs_id = int(params.get('parent_wbs_id')) if params.get('parent_wbs_id') else None
        self.ev_user_pct = _s('ev_user_pct')
        self.ev_etc_user_value = _s('ev_etc_user_value')
        self.orig_cost = _s('orig_cost')
        self.indep_remain_total_cost = _s('indep_remain_total_cost')
        self.ann_dscnt_rate_pct = _s('ann_dscnt_rate_pct')
        self.dscnt_period_type = _s('dscnt_period_type')
        self.indep_remain_work_qty = _s('indep_remain_work_qty')
        self.anticip_start_date = _s('anticip_start_date')
        self.anticip_end_date = _s('anticip_end_date')
        self.ev_compute_type = _s('ev_compute_type')
        self.ev_etc_compute_type = _s('ev_etc_compute_type')
        self.guid = _s('guid')
        self.tmpl_guid = _s('tmpl_guid')
        self.plan_open_state = _s('plan_open_state')
        self.data = data
        WBS.obj_list.append(self)

# Spec fields appended for Oracle data-map compliance (stored raw for lossless round-trip)
        self.status_reviewer = params.get('status_reviewer').strip() if params.get('status_reviewer') else None
    def get_id(self):
        return self.wbs_id

    def get_tsv(self):
        tsv = ['%R', self.wbs_id, self.proj_id, self.obs_id, self.seq_num, self.est_wt,
               self.proj_node_flag, self.sum_data_flag, self.status_code, self.wbs_short_name,
               self.wbs_name, self.phase_id, self.parent_wbs_id, self.ev_user_pct, self.ev_etc_user_value,
               self.orig_cost, self.indep_remain_total_cost, self.ann_dscnt_rate_pct, self.dscnt_period_type,
               self.indep_remain_work_qty, self.anticip_start_date, self.anticip_end_date, self.ev_compute_type,
               self.ev_etc_compute_type, self.guid, self.tmpl_guid, self.plan_open_state, self.status_reviewer]
        return tsv

    @classmethod
    def get_json(cls):
        root_nodes = list(filter(lambda x: WBS.find_by_id(x.parent_wbs_id) is None, cls.obj_list))
        json = dict()
        json["nodes"] = []
        for node in root_nodes:
            entry = {"node": node, "level": 0, "childs": [cls.get_childs(node, 0)]}
            json["nodes"].append(entry)
        return json

    @classmethod
    def get_childs(cls, node, level):
        nodes_lst = list(filter(lambda x: x.parent_wbs_id == node.wbs_id, cls.obj_list))
        childs = []
        for child in nodes_lst:
            childs.append({
                "node": child,
                "level": level + 1,
                "childs": [cls.get_childs(child, level + 1)],
            })
        return childs
    @classmethod
    def find_by_id(cls, ID):
        obj = list(filter(lambda x: x.wbs_id == ID, cls.obj_list))
        if obj:
            return obj[0]
        return None

    @classmethod
    def find_by_project_id(cls, project_id):
        return [ v for v in cls.obj_list if v.proj_id == project_id]

    @property
    def activities(self):
        return self.data.tasks.activities_by_wbs_id(self.wbs_id)

    def __repr__(self):
        return self.wbs_name
