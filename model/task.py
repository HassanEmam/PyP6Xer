class Task:
    task_id = ''
    proj_id = ''
    wbs_id = ''
    clndr_id = ''
    phys_complete_pct = ''
    rev_fdbk_flag = ''
    est_wt = ''
    lock_plan_flag = ''
    auto_compute_act_flag = ''
    complete_pct_type = ''
    task_type = ''
    duration_type = ''
    status_code = ''
    task_code = ''
    task_name = ''
    rsrc_id = ''
    total_float_hr_cnt = ''
    free_float_hr_cnt = ''
    remain_drtn_hr_cnt = ''
    act_work_qty = ''
    remain_work_qty = ''
    target_work_qty = ''
    target_drtn_hr_cnt = ''
    target_equip_qty = ''
    act_equip_qty = ''
    remain_equip_qty = ''
    cstr_date = ''
    act_start_date = ''
    act_end_date = ''
    late_start_date = ''
    late_end_date = ''
    expect_end_date = ''
    early_start_date = ''
    early_end_date = ''
    restart_date = ''
    reend_date = ''
    target_start_date = ''
    target_end_date = ''
    rem_late_start_date = ''
    rem_late_end_date = ''
    cstr_type = ''
    priority_type = ''
    suspend_date = ''
    resume_date = ''
    float_path = ''
    float_path_order = ''
    guid = ''
    tmpl_guid = ''
    cstr_date2 = ''
    cstr_type2 = ''
    driving_path_flag = ''
    act_this_per_work_qty = ''
    act_this_per_equip_qty = ''
    external_early_start_date = ''
    external_late_end_date = ''
    create_date = ''
    update_date = ''
    create_user = ''
    update_user = ''
    location_id = ''

    def __init__(self, params):
        self.task_id = params[0].strip()
        self.proj_id = params[1].strip()
        self.wbs_id = params[2].strip()
        self.clndr_id = params[3].strip()
        self.phys_complete_pct = params[4].strip()
        self.rev_fdbk_flag = params[5].strip()
        self.est_wt = params[6].strip()
        self.lock_plan_flag = params[7].strip()
        self.auto_compute_act_flag = params[8].strip()
        self.complete_pct_type = params[9].strip()
        self.task_type = params[10].strip()
        self.duration_type = params[11].strip()
        self.status_code = params[12].strip()
        self.task_code = params[13].strip()
        self.task_name = params[14].strip()
        self.rsrc_id = params[15].strip()
        self.total_float_hr_cnt = params[16].strip()
        self.free_float_hr_cnt = params[17].strip()
        self.remain_drtn_hr_cnt = params[18].strip()
        self.act_work_qty = params[19].strip()
        self.remain_work_qty = params[20].strip()
        self.target_work_qty = params[21].strip()
        self.target_drtn_hr_cnt = params[22].strip()
        self.target_equip_qty = params[23].strip()
        self.act_equip_qty = params[24].strip()
        self.remain_equip_qty = params[25].strip()
        self.cstr_date = params[26].strip()
        self.act_start_date = params[27].strip()
        self.act_end_date = params[28].strip()
        self.late_start_date = params[29].strip()
        self.late_end_date = params[30].strip()
        self.expect_end_date = params[31].strip()
        self.early_start_date = params[32].strip()
        self.early_end_date = params[33].strip()
        self.restart_date = params[34].strip()
        self.reend_date = params[35].strip()
        self.target_start_date = params[36].strip()
        self.target_end_date = params[37].strip()
        self.rem_late_start_date = params[38].strip()
        self.rem_late_end_date = params[39].strip()
        self.cstr_type = params[40].strip()
        self.priority_type = params[41].strip()
        self.suspend_date = params[42].strip()
        self.resume_date = params[43].strip()
        self.float_path = params[44].strip()
        self.float_path_order = params[45].strip()
        self.guid = params[46].strip()
        self.tmpl_guid = params[47].strip()
        self.cstr_date2 = params[48].strip()
        self.cstr_type2 = params[49].strip()
        self.driving_path_flag = params[50].strip()
        self.act_this_per_work_qty = params[51].strip()
        self.act_this_per_equip_qty = params[52].strip()
        self.external_early_start_date = params[53].strip()
        self.external_late_end_date = params[54].strip()
        self.create_date = params[55].strip()
        self.update_date = params[56].strip()
        self.create_user = params[57].strip()
        self.update_user = params[58].strip()
        self.location_id = params[59].strip()

    def get_id(self):
        return self.task_id

    @staticmethod
    def find_by_activity_id(activity_id, tasks_dict):
        search = {k: v for k, v in tasks_dict.items() if v.task_code == activity_id}
        k = list(search.keys())[0]
        return search[k]

    def get_float(self):
        return float(self.total_float_hr_cnt)/8.0

    def __repr__(self):
        return self.task_code
