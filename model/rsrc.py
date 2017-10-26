class Resource:
    obj_list = []

    def __init__(self, params):
        self.rsrc_id = params[0].strip()
        self.parent_rsrc_id = params[1].strip()
        self.clndr_id = params[2].strip()
        self.role_id = params[3].strip()
        self.shift_id = params[4].strip()
        self.user_id = params[5].strip()
        self.pobs_id = params[6].strip()
        self.guid = params[7].strip()
        self.rsrc_seq_num = params[8].strip()
        self.email_addr = params[9].strip()
        self.employee_code = params[10].strip()
        self.office_phone = params[11].strip()
        self.other_phone = params[12].strip()
        self.rsrc_name = params[13].strip()
        self.rsrc_short_name = params[14].strip()
        self.rsrc_title_name = params[15].strip()
        self.def_qty_per_hr = params[16].strip()
        self.cost_qty_type = params[17].strip()
        self.ot_factor = params[18].strip()
        self.active_flag = params[19].strip()
        self.auto_compute_act_flag = params[20].strip()
        self.def_cost_qty_link_flag = params[21].strip()
        self.ot_flag = params[22].strip()
        self.curr_id = params[23].strip()
        self.unit_id = params[24].strip()
        self.rsrc_type = params[25].strip()
        self.location_id = params[26].strip()
        self.rsrc_notes = params[27].strip()
        self.load_tasks_flag = params[28].strip()
        self.level_flag = params[29].strip()
        self.last_checksum = params[30].strip()
        Resource.obj_list.append(self)

    def get_id(self):
        return self.rsrc_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.rsrc_name