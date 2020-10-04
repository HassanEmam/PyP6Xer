

class Role:
    obj_list = []

    def __init__(self, params):
        self.role_id = int(params[0]) if params[0] else None
        self.parent_role_id = int(params[1]) if params[1] else None
        self.seq_num = int(params[2]) if params[2] else None
        self.role_name = params[3].strip()
        self.role_short_name = params[4].strip()
        self.pobs_id = params[5]
        self.def_cost_qty_link_flag = params[6].strip()
        self.cost_qty_type = params[7].strip()
        self.role_descr = params[8].strip()
        self.last_checksum = params[9].strip()

        Role.obj_list.append(self)

    def __repr__(self):
        return self.role_name
