class WBS:
    obj_list = []

    def __init__(self, params):
        self.wbs_id = int(params[0].strip()) if params[0] else None
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

        WBS.obj_list.append(self)

    def get_id(self):
        return self.wbs_id

    @classmethod
    def find_by_id(cls, ID):
        obj = list(filter(lambda x: x.wbs_id == ID, cls.obj_list))

        print(obj)
        if obj:
            return obj[0]
        return None

    @staticmethod
    def find_by_project_id(project_id, wbs):
        return {k: v for k, v in wbs.items() if v.proj_id == project_id}


    def __repr__(self):
        return self.wbs_name
