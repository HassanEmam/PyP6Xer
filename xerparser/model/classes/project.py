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
from xerparser.model.tasks import Tasks
from xerparser.model.wbss import WBSs

class Project:

    def __init__(self, params, data):

        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None
        self.fy_start_month_num = params.get('fy_start_month_num').strip() if params.get('fy_start_month_num') else None
        self.rsrc_self_add_flag = params.get('rsrc_self_add_flag').strip() if params.get('rsrc_self_add_flag') else None
        self.allow_complete_flag = params.get('allow_complete_flag').strip() if params.get('allow_complete_flag') else None
        self.rsrc_multi_assign_flag = params.get('rsrc_multi_assign_flag').strip() if params.get('rsrc_multi_assign_flag') else None
        self.checkout_flag = params.get('checkout_flag').strip() if params.get('checkout_flag') else None
        self.project_flag = params.get('project_flag').strip() if params.get('project_flag') else None
        self.step_complete_flag = params.get('step_complete_flag').strip() if params.get('step_complete_flag') else None
        self.cost_qty_recalc_flag = params.get('cost_qty_recalc_flag').strip() if params.get('cost_qty_recalc_flag') else None
        self.batch_sum_flag = params.get('batch_sum_flag').strip() if params.get('batch_sum_flag') else None
        self.name_sep_char = params.get('name_sep_char').strip() if params.get('name_sep_char') else None
        self.def_complete_pct_type = params.get('def_complete_pct_type').strip() if params.get('def_complete_pct_type') else None
        self.proj_short_name = params.get('proj_short_name').strip() if params.get('proj_short_name') else None
        self.acct_id = params.get('acct_id').strip() if params.get('acct_id') else None
        self.orig_proj_id = params.get('orig_proj_id').strip() if params.get('orig_proj_id') else None
        self.source_proj_id = params.get('source_proj_id').strip() if params.get('source_proj_id') else None
        self.base_type_id = params.get('base_type_id').strip() if params.get('base_type_id') else None
        self.clndr_id = params.get('clndr_id').strip() if params.get('clndr_id') else None
        self.sum_base_proj_id = params.get('sum_base_proj_id').strip() if params.get('sum_base_proj_id') else None
        self.task_code_base = params.get('task_code_base').strip() if params.get('task_code_base') else None
        self.task_code_step = params.get('task_code_step').strip() if params.get('task_code_step') else None
        self.priority_num = params.get('priority_num').strip() if params.get('priority_num') else None
        self.wbs_max_sum_level = params.get('wbs_max_sum_level').strip() if params.get('wbs_max_sum_level') else None
        self.strgy_priority_num = params.get('strgy_priority_num').strip() if params.get('strgy_priority_num') else None
        self.last_checksum = params.get('last_checksum').strip() if params.get('last_checksum') else None
        self.critical_drtn_hr_cnt = params.get('critical_drtn_hr_cnt').strip() if params.get('critical_drtn_hr_cnt') else None
        self.def_cost_per_qty = params.get('def_cost_per_qty').strip() if params.get('def_cost_per_qty') else None
        self.last_recalc_date = params.get('last_recalc_date').strip() if params.get('last_recalc_date') else None
        self.plan_start_date = params.get('plan_start_date').strip() if params.get('plan_start_date') else None
        self.plan_end_date = params.get('plan_end_date').strip() if params.get('plan_end_date') else None
        self.scd_end_date = params.get('scd_end_date').strip() if params.get('scd_end_date') else None
        self.add_date = params.get('add_date').strip() if params.get('add_date') else None
        self.last_tasksum_date = params.get('last_tasksum_date').strip() if params.get('last_tasksum_date') else None
        self.fcst_start_date = params.get('fcst_start_date').strip() if params.get('fcst_start_date') else None
        self.def_duration_type = params.get('def_duration_type').strip() if params.get('def_duration_type') else None
        self.task_code_prefix = params.get('task_code_prefix').strip() if params.get('task_code_prefix') else None
        self.guid = params.get('guid').strip() if params.get('guid') else None
        self.def_qty_type = params.get('def_qty_type').strip() if params.get('def_qty_type') else None
        self.add_by_name = params.get('add_by_name').strip() if params.get('add_by_name') else None
        self.web_local_root_path = params.get('web_local_root_path').strip() if params.get('web_local_root_path') else None
        self.proj_url = params.get('proj_url').strip() if params.get('proj_url') else None
        self.def_rate_type = params.get('def_rate_type').strip() if params.get('def_rate_type') else None
        self.add_act_remain_flag = params.get('add_act_remain_flag').strip() if params.get('add_act_remain_flag') else None
        self.act_this_per_link_flag = params.get('act_this_per_link_flag').strip() if params.get('act_this_per_link_flag') else None
        self.def_task_type = params.get('def_task_type').strip() if params.get('def_task_type') else None
        self.act_pct_link_flag = params.get('act_pct_link_flag').strip() if params.get('act_pct_link_flag') else None
        self.critical_path_type = params.get('critical_path_type').strip() if params.get('critical_path_type') else None
        self.task_code_prefix_flag = params.get('task_code_prefix_flag').strip() if params.get('task_code_prefix_flag') else None
        self.def_rollup_dates_flag = params.get('def_rollup_dates_flag').strip() if params.get('def_rollup_dates_flag') else None
        self.use_project_baseline_flag = params.get('use_project_baseline_flag').strip() if params.get('use_project_baseline_flag') else None
        self.rem_target_link_flag = params.get('rem_target_link_flag').strip() if params.get('rem_target_link_flag') else None
        self.reset_planned_flag = params.get('reset_planned_flag').strip() if params.get('reset_planned_flag') else None
        self.allow_neg_act_flag = params.get('allow_neg_act_flag').strip() if params.get('allow_neg_act_flag') else None
        self.sum_assign_level = params.get('sum_assign_level').strip() if params.get('sum_assign_level') else None
        self.last_fin_dates_id = params.get('last_fin_dates_id').strip() if params.get('last_fin_dates_id') else None
        self.last_baseline_update_date = params.get('last_fin_dates_id').strip() if params.get('last_fin_dates_id') else None
        self.cr_external_key = params.get('cr_external_key').strip() if params.get('cr_external_key') else None
        self.apply_actuals_date = params.get('apply_actuals_date').strip() if params.get('apply_actuals_date') else None
        self.location_id = params.get('location_id') if params.get('location_id') else None
        self.loaded_scope_level = params.get('loaded_scope_level').strip() if params.get('loaded_scope_level') else None
        self.export_flag = params.get('export_flag').strip() if params.get('export_flag') else None
        self.new_fin_dates_id = params.get('new_fin_dates_id').strip() if params.get('new_fin_dates_id') else None
        self.baselines_to_export = params.get('baselines_to_export').strip() if params.get('baselines_to_export') else None
        self.baseline_names_to_export = params.get('baseline_names_to_export').strip() if params.get('baseline_names_to_export') else None
        self.next_data_date = params.get('next_data_date').strip() if params.get('next_data_date') else None
        self.close_period_flag = params.get('close_period_flag').strip() if params.get('close_period_flag') else None
        self.sum_refresh_date = params.get('sum_refresh_date').strip() if params.get('sum_refresh_date') else None
        self.trsrcsum_loaded = params.get('trsrcsum_loaded').strip() if params.get('trsrcsum_loaded') else None
        self.fintmpl_id = int(params.get('fintmpl_id').strip()) if params.get('fintmpl_id') else None
        self.sumtask_loaded = params.get('sumtask_loaded').strip() if params.get('sumtask_loaded') else None
        self.data = data

    @property
    def id(self):
        return self.proj_id

    def get_tsv(self):
        tsv = ['%R', self.proj_id, self.fy_start_month_num, self.rsrc_self_add_flag,
               self.allow_complete_flag, self.rsrc_multi_assign_flag, self.checkout_flag,
               self.project_flag, self.step_complete_flag, self.cost_qty_recalc_flag,
               self.batch_sum_flag, self.name_sep_char, self.def_complete_pct_type, self.proj_short_name,
               self.acct_id, self.orig_proj_id, self.source_proj_id, self.base_type_id, self.clndr_id,
               self.sum_base_proj_id, self.task_code_base, self.task_code_step, self.priority_num,
               self.wbs_max_sum_level, self.strgy_priority_num, self.last_checksum, self.critical_drtn_hr_cnt,
               self.def_cost_per_qty, self.last_recalc_date, self.plan_start_date, self.plan_end_date,
               self.scd_end_date, self.add_date, self.last_tasksum_date, self.fcst_start_date, self.def_duration_type,
               self.task_code_prefix, self.guid, self.def_qty_type, self.add_by_name, self.web_local_root_path,
               self.proj_url, self.def_rate_type, self.add_act_remain_flag, self.act_this_per_link_flag,
               self.def_task_type, self.act_pct_link_flag, self.critical_path_type, self.task_code_prefix_flag,
               self.def_rollup_dates_flag, self.use_project_baseline_flag, self.rem_target_link_flag,
               self.reset_planned_flag, self.allow_neg_act_flag, self.sum_assign_level, self.last_fin_dates_id,
               self.last_baseline_update_date, self.cr_external_key, self.apply_actuals_date, self.fintmpl_id,
               self.location_id, self.loaded_scope_level, self.export_flag, self.new_fin_dates_id,
               self.baselines_to_export, self.baseline_names_to_export, self.next_data_date, self.close_period_flag,
               self.sum_refresh_date, self.trsrcsum_loaded, self.sumtask_loaded]
        return tsv

    @property
    def activities(self):
        return self.data.tasks.get_by_project(self.proj_id)

    @property
    def wbss(self):
        # wbss = WBSs()
        return self.data.wbss.get_by_project(self.proj_id)

    def __repr__(self):
        return self.proj_short_name