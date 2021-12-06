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


from xerparser.model.resources import Resources
class TaskRsrc:

    def __init__(self, params, data=None):
        self.taskrsrc_id = int(params.get('taskrsrc_id').strip()) if params.get('taskrsrc_id') else None
        self.task_id = int(params.get('task_id').strip()) if params.get('task_id') else None
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.cost_qty_link_flag = params.get('cost_qty_link_flag').strip() if params.get('cost_qty_link_flag') else None
        self.role_id = params.get('role_id').strip() if params.get('role_id') else None
        self.acct_id = params.get('acct_id').strip() if params.get('acct_id') else None
        self.rsrc_id = int(params.get('rsrc_id').strip()) if params.get('rsrc_id') else None
        self.pobs_id = params.get('pobs_id').strip() if params.get('pobs_id') else None
        self.skill_level = params.get('skill_level').strip() if params.get('skill_level') else None
        self.remain_qty = float(params.get('remain_qty').strip()) if params.get('remain_qty') else None
        self.target_qty = float(params.get('target_qty').strip()) if params.get('target_qty') else None
        self.remain_qty_per_hr = float(params.get('remain_qty_per_hr').strip()) if params.get('remain_qty_per_hr') else None
        self.target_lag_drtn_hr_cnt = float(params.get('target_lag_drtn_hr_cnt').strip()) if params.get('target_lag_drtn_hr_cnt') else None
        self.target_qty_per_hr = params.get('target_qty_per_hr').strip() if params.get('target_qty_per_hr') else None
        self.act_ot_qty = params.get('act_ot_qty').strip() if params.get('act_ot_qty') else None
        self.act_reg_qty = params.get('act_reg_qty').strip() if params.get('act_reg_qty') else None
        self.relag_drtn_hr_cnt = params.get('relag_drtn_hr_cnt').strip() if params.get('relag_drtn_hr_cnt') else None
        self.ot_factor = params.get('ot_factor').strip() if params.get('ot_factor') else None
        self.cost_per_qty = params.get('cost_per_qty').strip() if params.get('cost_per_qty') else None
        self.target_cost = params.get('target_cost').strip() if params.get('target_cost') else None
        self.act_reg_cost = float(params.get('act_reg_cost').strip()) if params.get('act_reg_cost') else None
        self.act_ot_cost = params.get('act_ot_cost').strip() if params.get('act_ot_cost') else None
        self.remain_cost = params.get('remain_cost').strip() if params.get('remain_cost') else None
        self.act_start_date = params.get('act_start_date').strip() if params.get('act_start_date') else None
        self.act_end_date = params.get('act_end_date').strip() if params.get('act_end_date') else None
        self.restart_date = params.get('restart_date').strip() if params.get('restart_date') else None
        self.reend_date = params.get('reend_date').strip() if params.get('reend_date') else None
        self.target_start_date = params.get('target_start_date').strip() if params.get('target_start_date') else None
        self.target_end_date = params.get('target_end_date').strip() if params.get('target_end_date') else None
        self.rem_late_start_date = params.get('rem_late_start_date').strip() if params.get('rem_late_start_date') else None
        self.rem_late_end_date = params.get('rem_late_end_date').strip() if params.get('rem_late_end_date') else None
        self.rollup_dates_flag = params.get('rollup_dates_flag').strip() if params.get('rollup_dates_flag') else None
        self.target_crv = params.get('target_crv').strip() if params.get('target_crv') else None
        self.remain_crv = params.get('remain_crv').strip() if params.get('remain_crv') else None
        self.actual_crv = params.get('actual_crv').strip() if params.get('actual_crv') else None
        self.ts_pend_act_end_flag = params.get('ts_pend_act_end_flag').strip() if params.get('ts_pend_act_end_flag') else None
        self.guid = params.get('guid').strip() if params.get('guid') else None
        self.rate_type = params.get('rate_type').strip() if params.get('rate_type') else None
        self.act_this_per_cost = params.get('act_this_per_cost').strip() if params.get('act_this_per_cost') else None
        self.act_this_per_qty = params.get('act_this_per_cost').strip() if params.get('act_this_per_cost') else None
        self.curv_id = params.get('curv_id').strip() if params.get('curv_id') else None
        self.rsrc_type = params.get('rsrc_type').strip() if params.get('rsrc_type') else None
        self.cost_per_qty_source_type = params.get('cost_per_qty_source_type').strip() if params.get('cost_per_qty_source_type') else None
        self.create_user = params.get('create_user').strip() if params.get('create_user') else None
        self.create_date = params.get('create_date').strip() if params.get('create_date') else None
        self.cbs_id = params.get('cbs_id').strip() if params.get('cbs_id') else None
        self.has_rsrchours = params.get('has_rsrchours').strip() if params.get('has_rsrchours') else None
        self.taskrsrc_sum_id = params.get('taskrsrc_sum_id').strip() if params.get('taskrsrc_sum_id') else None
        self.data = data

    def get_id(self):
        return self.taskrsrc_id
    @property
    def resource(self):
        return self.data.resources.get_resource_by_id(self.rsrc_id)

    def get_tsv(self):
        tsv = ['%R', self.taskrsrc_id, self.task_id, self.proj_id, self.cost_qty_link_flag, self.role_id, self.acct_id,
               self.rsrc_id, self.pobs_id, self.skill_level, self.remain_qty, self.target_qty, self.remain_qty_per_hr,
               self.target_lag_drtn_hr_cnt, self.target_qty_per_hr, self.act_ot_qty, self.act_reg_qty,
               self.relag_drtn_hr_cnt, self.ot_factor, self.cost_per_qty, self.target_cost, self.act_reg_cost,
               self.act_ot_cost, self.remain_cost, self.act_start_date, self.act_end_date, self.restart_date,
               self.reend_date, self.target_start_date, self.target_end_date, self.rem_late_start_date,
               self.rem_late_end_date, self.rollup_dates_flag, self.target_crv, self.remain_crv, self.actual_crv,
               self.ts_pend_act_end_flag, self.guid, self.rate_type, self.act_this_per_cost, self.act_this_per_qty,
               self.curv_id, self.rsrc_type, self.cost_per_qty_source_type, self.create_user, self.create_date,
               self.cbs_id, self.has_rsrchours, self.taskrsrc_sum_id]
        return tsv

    def __repr__(self):
        return str(self.task_id) + '->' + str(self.rsrc_id) + ' = ' + str(self.target_qty)
