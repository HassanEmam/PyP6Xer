from xerparser.model.wbss import WBSs
from xerparser.model.tasks import Tasks

class Project:
    obj_list = []

    def __init__(self, params):

        self.proj_id = int(params[0].strip()) if params[0].strip() else None
        self.fy_start_month_num = params[1].strip()
        self.rsrc_self_add_flag = params[2].strip()
        self.allow_complete_flag = params[3].strip()
        self.rsrc_multi_assign_flag = params[4].strip()
        self.checkout_flag = params[5].strip()
        self.project_flag = params[6].strip()
        self.step_complete_flag = params[7].strip()
        self.cost_qty_recalc_flag = params[8].strip()
        self.batch_sum_flag = params[9].strip()
        self.name_sep_char = params[10].strip()
        self.def_complete_pct_type = params[11].strip()
        self.proj_short_name = params[12].strip()
        self.acct_id = params[13].strip()
        self.orig_proj_id = params[14].strip()
        self.source_proj_id = params[15].strip()
        self.base_type_id = params[16].strip()
        self.clndr_id = params[17].strip()
        self.sum_base_proj_id = params[18].strip()
        self.task_code_base = params[19].strip()
        self.task_code_step = params[20].strip()
        self.priority_num = params[21].strip()
        self.wbs_max_sum_level = params[22].strip()
        self.strgy_priority_num = params[23].strip()
        self.last_checksum = params[24].strip()
        self.critical_drtn_hr_cnt = params[25].strip()
        self.def_cost_per_qty = params[26].strip()
        self.last_recalc_date = params[27].strip()
        self.plan_start_date = params[28].strip()
        self.plan_end_date = params[29].strip()
        self.scd_end_date = params[30].strip()
        self.add_date = params[31].strip()
        self.last_tasksum_date = params[32].strip()
        self.fcst_start_date = params[33].strip()
        self.def_duration_type = params[34].strip()
        self.task_code_prefix = params[35].strip()
        self.guid = params[36].strip()
        self.def_qty_type = params[37].strip()
        self.add_by_name = params[38].strip()
        self.web_local_root_path = params[39].strip()
        self.proj_url = params[40].strip()
        self.def_rate_type = params[41].strip()
        self.add_act_remain_flag = params[42].strip()
        self.act_this_per_link_flag = params[43].strip()
        self.def_task_type = params[44].strip()
        self.act_pct_link_flag = params[45].strip()
        self.critical_path_type = params[46].strip()
        self.task_code_prefix_flag = params[47].strip()
        self.def_rollup_dates_flag = params[48].strip()
        self.use_project_baseline_flag = params[49].strip()
        self.rem_target_link_flag = params[50].strip()
        self.reset_planned_flag = params[51].strip()
        self.allow_neg_act_flag = params[52].strip()
        self.sum_assign_level = params[53].strip()
        self.last_fin_dates_id = params[54].strip()
        self.last_baseline_update_date = params[55].strip()
        self.cr_external_key = params[56].strip()
        self.apply_actuals_date = params[57].strip()
        self.location_id = params[58].strip()
        self.loaded_scope_level = params[59].strip()
        self.export_flag = params[60].strip()
        self.new_fin_dates_id = params[61].strip()
        self.baselines_to_export = params[62].strip()
        self.baseline_names_to_export = params[63].strip()
        self.next_data_date = params[64].strip()
        self.close_period_flag = params[65].strip()
        self.sum_refresh_date = params[66].strip()
        self.trsrcsum_loaded = params[67].strip()
        Project.obj_list.append(self)

    @property
    def id(self):
        return self.proj_id


    @property
    def activities(self):
        return Tasks.get_by_project(self.proj_id)

    @property
    def wbss(self):
        return WBSs.get_by_project(self.proj_id)


    def __repr__(self):
        return self.proj_short_name