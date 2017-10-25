class WBS:
    wbs_id = ''
    proj_id = ''
    obs_id = ''
    seq_num = ''
    est_wt = ''
    proj_node_flag = ''
    sum_data_flag = ''
    status_code = ''
    wbs_short_name = ''
    wbs_name = ''
    phase_id = ''
    parent_wbs_id = ''
    ev_user_pct = ''
    ev_etc_user_value = ''
    orig_cost = ''
    indep_remain_total_cost = ''
    ann_dscnt_rate_pct = ''
    dscnt_period_type = ''
    indep_remain_work_qty = ''
    anticip_start_date = ''
    anticip_end_date = ''
    ev_compute_type = ''
    ev_etc_compute_type = ''
    guid = ''
    tmpl_guid = ''
    plan_open_state = ''

    def __init__(self, params):
        self.wbs_id = params[0].strip()
        self.proj_id = params[1].strip()
        self.obs_id = params[2].strip()
        self.seq_num = params[3].strip()
        self.est_wt = params[4].strip()
        self.proj_node_flag = params[5].strip()
        self.sum_data_flag = params[6].strip()
        self.status_code = params[7].strip()
        self.wbs_short_name = params[8].strip()
        self.wbs_name = params[9].strip()
        self.phase_id = params[10].strip()
        self.parent_wbs_id = params[11].strip()
        self.ev_user_pct = params[12].strip()
        self.ev_etc_user_value = params[13].strip()
        self.orig_cost = params[14].strip()
        self.indep_remain_total_cost = params[15].strip()
        self.ann_dscnt_rate_pct = params[16].strip()
        self.dscnt_period_type = params[17].strip()
        self.indep_remain_work_qty = params[18].strip()
        self.anticip_start_date = params[19].strip()
        self.anticip_end_date = params[20].strip()
        self.ev_compute_type = params[21].strip()
        self.ev_etc_compute_type = params[22].strip()
        self.guid = params[23].strip()
        self.tmpl_guid = params[24].strip()
        self.plan_open_state = params[25].strip()

    def get_id(self):
        return self.wbs_id

    @staticmethod
    def find_by_project_id(project_id, wbs):
        return {k: v for k, v in wbs.items() if v.proj_id == project_id}


    def __repr__(self):
        return self.wbs_name