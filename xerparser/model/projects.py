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


from xerparser.model.classes.project import Project
from xerparser.model.classes.data import Data

class Projects:


    def __init__(self):
        self.index =0
        self._projects = []

    def add(self, params, data):
        prj = Project(params, data)
        self._projects.append(prj)

    def get_tsv(self):
        if len(self._projects):
            tsv = []
            tsv.append(['%T', 'PROJECT'])
            tsv.append(['%F', 'proj_id', 'fy_start_month_num', 'rsrc_self_add_flag',
                   'allow_complete_flag', 'rsrc_multi_assign_flag', 'checkout_flag',
                   'project_flag', 'step_complete_flag', 'cost_qty_recalc_flag',
                   'batch_sum_flag', 'name_sep_char', 'def_complete_pct_type', 'proj_short_name',
                   'acct_id', 'orig_proj_id', 'source_proj_id', 'base_type_id', 'clndr_id',
                   'sum_base_proj_id', 'task_code_base', 'task_code_step', 'priority_num',
                   'wbs_max_sum_level', 'strgy_priority_num', 'last_checksum', 'critical_drtn_hr_cnt',
                   'def_cost_per_qty', 'last_recalc_date', 'plan_start_date', 'plan_end_date',
                   'scd_end_date', 'add_date', 'last_tasksum_date', 'fcst_start_date', 'def_duration_type',
                   'task_code_prefix', 'guid', 'def_qty_type', 'add_by_name', 'web_local_root_path',
                   'proj_url', 'def_rate_type', 'add_act_remain_flag', 'act_this_per_link_flag',
                   'def_task_type', 'act_pct_link_flag', 'critical_path_type', 'task_code_prefix_flag',
                   'def_rollup_dates_flag', 'use_project_baseline_flag', 'rem_target_link_flag',
                   'reset_planned_flag', 'allow_neg_act_flag', 'sum_assign_level', 'last_fin_dates_id',
                   'last_baseline_update_date', 'cr_external_key', 'apply_actuals_date', 'fintmpl_id', 'location_id',
                   'loaded_scope_level', 'export_flag', 'new_fin_dates_id', 'baselines_to_export',
                   'baseline_names_to_export', 'next_data_date', 'close_period_flag', 'sum_refresh_date',
                   'trsrcsum_loaded', 'sumtask_loaded'])
            for prj in self._projects:
                tsv.append(prj.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> Project:
        obj = list(filter(lambda x: x.proj_id == id, self._projects))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return str(self._projects)

    def __iter__(self):
        return self

    def __next__(self) -> Project:
        if self.index >= len(self._projects):
            raise StopIteration
        idx = self.index
        self.index +=1
        return self._projects[idx]