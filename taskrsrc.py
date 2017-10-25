class TaskRsrc:
    taskrsrc_id = ''
    task_id = ''
    proj_id = ''
    cost_qty_link_flag = ''
    role_id = ''
    acct_id = ''
    rsrc_id = ''
    pobs_id = ''
    skill_level = ''
    remain_qty = ''
    target_qty = ''
    remain_qty_per_hr = ''
    target_lag_drtn_hr_cnt = ''
    target_qty_per_hr = ''
    act_ot_qty = ''
    act_reg_qty = ''
    relag_drtn_hr_cnt = ''
    ot_factor = ''
    cost_per_qty = ''
    target_cost = ''
    act_reg_cost = ''
    act_ot_cost = ''
    remain_cost = ''
    act_start_date = ''
    act_end_date = ''
    restart_date = ''
    reend_date = ''
    target_start_date = ''
    target_end_date = ''
    rem_late_start_date = ''
    rem_late_end_date = ''
    rollup_dates_flag = ''
    target_crv = ''
    remain_crv = ''
    actual_crv = ''
    ts_pend_act_end_flag = ''
    guid = ''
    rate_type = ''
    act_this_per_cost = ''
    act_this_per_qty = ''
    curv_id = ''
    rsrc_type = ''
    cost_per_qty_source_type = ''
    create_user = ''
    create_date = ''
    has_rsrchours = ''
    taskrsrc_sum_id = ''

    def __init__(self, params):
        self.taskrsrc_id = params[0].strip()
        self.task_id = params[1].strip()
        self.proj_id = params[2].strip()
        self.cost_qty_link_flag = params[3].strip()
        self.role_id = params[4].strip()
        self.acct_id = params[5].strip()
        self.rsrc_id = params[6].strip()
        self.pobs_id = params[7].strip()
        self.skill_level = params[8].strip()
        self.remain_qty = params[9].strip()
        self.target_qty = params[10].strip()
        self.remain_qty_per_hr = params[11].strip()
        self.target_lag_drtn_hr_cnt = params[12].strip()
        self.target_qty_per_hr = params[13].strip()
        self.act_ot_qty = params[14].strip()
        self.act_reg_qty = params[15].strip()
        self.relag_drtn_hr_cnt = params[16].strip()
        self.ot_factor = params[17].strip()
        self.cost_per_qty = params[18].strip()
        self.target_cost = params[19].strip()
        self.act_reg_cost = params[20].strip()
        self.act_ot_cost = params[21].strip()
        self.remain_cost = params[22].strip()
        self.act_start_date = params[23].strip()
        self.act_end_date = params[24].strip()
        self.restart_date = params[25].strip()
        self.reend_date = params[26].strip()
        self.target_start_date = params[27].strip()
        self.target_end_date = params[28].strip()
        self.rem_late_start_date = params[29].strip()
        self.rem_late_end_date = params[30].strip()
        self.rollup_dates_flag = params[31].strip()
        self.target_crv = params[32].strip()
        self.remain_crv = params[33].strip()
        self.actual_crv = params[34].strip()
        self.ts_pend_act_end_flag = params[35].strip()
        self.guid = params[36].strip()
        self.rate_type = params[37].strip()
        self.act_this_per_cost = params[38].strip()
        self.act_this_per_qty = params[39].strip()
        self.curv_id = params[40].strip()
        self.rsrc_type = params[41].strip()
        self.cost_per_qty_source_type = params[42].strip()
        self.create_user = params[43].strip()
        self.create_date = params[44].strip()
        self.has_rsrchours = params[45].strip()
        self.taskrsrc_sum_id = params[46].strip()

    def get_id(self):
        return self.taskrsrc_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.task_id + '->' + self.rsrc_id + ' = ' + self.target_qty
