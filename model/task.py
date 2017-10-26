class Task:
    obj_list = []

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
        self.total_float_hr_cnt = float(params[16].strip()) if params[16] else None
        self.free_float_hr_cnt = params[17].strip()
        self.remain_drtn_hr_cnt = float(params[18].strip()) if params[18] else None
        self.act_work_qty = params[19].strip()
        self.remain_work_qty = params[20].strip()
        self.target_work_qty = params[21].strip()
        self.target_drtn_hr_cnt = float(params[22].strip()) if params[18] else None
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
        Task.obj_list.append(self)

    def get_id(self):
        return self.task_id

    def get_float(self):
        if self.total_float_hr_cnt:
            tf = float(self.total_float_hr_cnt)/8.0
        else:
            return None
        return tf

    def get_duration(self):
        dur = None
        if self.target_drtn_hr_cnt:
            dur = float(self.target_drtn_hr_cnt)/8.0
        return dur

    def constraints(self):
        return {"ConstraintType": self.cstr_type,
                "ConstrintDate": self.cstr_date}
    def start_date(self):
        if self.act_start_date:
            return self.act_start_date
        else:
            return self.target_start_date
    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.task_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    @classmethod
    def find_by_code(cls, code):
        obj = list(filter(lambda x: x.task_code == code, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    @classmethod
    def duration_greater_than(cls, duration):
        obj = list(filter(lambda x: x.target_drtn_hr_cnt > duration*8, cls.obj_list))
        if obj:
            return obj
        return obj

    @classmethod
    def float_less_than(cls, Tfloat):
        objs = list(filter(lambda x: x.status_code != "TK_Complete" , cls.obj_list))
        obj = list(filter(lambda x: x.total_float_hr_cnt < Tfloat * 8, objs))
        if obj:
            return obj
        return obj

    @classmethod
    def float_greater_than(cls, Tfloat):
        objs = list(filter(lambda x: x.status_code != "TK_Complete", cls.obj_list))
        obj = list(filter(lambda x: x.total_float_hr_cnt > Tfloat * 8, objs))
        if obj:
            return obj
        return obj

    @classmethod
    def float_within_range(cls, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", cls.obj_list))
        if float1 < float2:
            obj = list(filter(lambda x: x.total_float_hr_cnt >= float1 * 8 and x.total_float_hr_cnt <= float2 * 8, objs))
            if obj:
                return obj
        return obj

    @classmethod
    def float_within_range_exclusive(cls, float1, float2):
        obj = None
        objs = list(filter(lambda x: x.status_code != "TK_Complete", cls.obj_list))
        if float1 < float2:
            obj = list(filter(lambda x: x.total_float_hr_cnt > float1 * 8 and x.total_float_hr_cnt < float2 * 8, objs))
            if obj:
                return obj
        return obj
    def __repr__(self):
        return self.task_code
