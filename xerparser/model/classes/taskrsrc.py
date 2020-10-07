class TaskRsrc:
    taskrsrc_id = None
    task_id = None
    proj_id = None
    cost_qty_link_flag = None
    role_id = None
    acct_id = None
    rsrc_id = None
    pobs_id = None
    skill_level = None
    remain_qty = None
    target_qty = None
    remain_qty_per_hr = None
    target_lag_drtn_hr_cnt = None
    target_qty_per_hr = None
    act_ot_qty = None
    act_reg_qty = None
    relag_drtn_hr_cnt = None
    ot_factor = None
    cost_per_qty = None
    target_cost = None
    act_reg_cost = None
    act_ot_cost = None
    remain_cost = None
    act_start_date = None
    act_end_date = None
    restart_date = None
    reend_date = None
    target_start_date = None
    target_end_date = None
    rem_late_start_date = None
    rem_late_end_date = None
    rollup_dates_flag = None
    target_crv = None
    remain_crv = None
    actual_crv = None
    ts_pend_act_end_flag = None
    guid = None
    rate_type = None
    act_this_per_cost = None
    act_this_per_qty = None
    curv_id = None
    rsrc_type = None
    cost_per_qty_source_type = None
    create_user = None
    create_date = None
    has_rsrchours = None
    taskrsrc_sum_id = None

    def __init__(self, params):
        self.taskrsrc_id = params.get('taskrsrc_id').strip() if params.get('taskrsrc_id') else None
        self.task_id = params.get('task_id').strip() if params.get('task_id') else None
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.cost_qty_link_flag = params.get('cost_qty_link_flag').strip() if params.get('cost_qty_link_flag') else None
        self.role_id = params.get('role_id').strip() if params.get('role_id') else None
        self.acct_id = params.get('acct_id').strip() if params.get('acct_id') else None
        self.rsrc_id = params.get('rsrc_id').strip() if params.get('rsrc_id') else None
        self.pobs_id = params.get('pobs_id').strip() if params.get('pobs_id') else None
        self.skill_level = params.get('skill_level').strip() if params.get('skill_level') else None
        self.remain_qty = params.get('remain_qty').strip() if params.get('remain_qty') else None
        self.target_qty = params.get('target_qty').strip() if params.get('target_qty') else None
        self.remain_qty_per_hr = params.get('remain_qty_per_hr').strip() if params.get('remain_qty_per_hr') else None
        self.target_lag_drtn_hr_cnt = params.get('target_lag_drtn_hr_cnt').strip() if params.get('target_lag_drtn_hr_cnt') else None
        self.target_qty_per_hr = params.get('target_qty_per_hr').strip() if params.get('target_qty_per_hr') else None
        self.act_ot_qty = params.get('act_ot_qty').strip() if params.get('act_ot_qty') else None
        self.act_reg_qty = params.get('act_reg_qty').strip() if params.get('act_reg_qty') else None
        self.relag_drtn_hr_cnt = params.get('relag_drtn_hr_cnt').strip() if params.get('relag_drtn_hr_cnt') else None
        self.ot_factor = params.get('ot_factor').strip() if params.get('ot_factor') else None
        self.cost_per_qty = params.get('cost_per_qty').strip() if params.get('cost_per_qty') else None
        self.target_cost = params.get('target_cost').strip() if params.get('target_cost') else None
        self.act_reg_cost = params.get('act_reg_cost').strip() if params.get('act_reg_cost') else None
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
        self.has_rsrchours = params.get('has_rsrchours').strip() if params.get('has_rsrchours') else None
        self.taskrsrc_sum_id = params.get('taskrsrc_sum_id').strip() if params.get('taskrsrc_sum_id') else None

    def get_id(self):
        return self.taskrsrc_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.task_id + '->' + self.rsrc_id + ' = ' + self.target_qty
