

class Role:
    obj_list = []

    def __init__(self, params):
        self.role_id = int(params[0]) if params[0] else None
        self.parent_role_id = params[1]
        self.seq_num = params[2]
        self.role_name = params[3]
        self.role_short_name = params[4]
        self.pobs_id = params[5]
        self.def_cost_qty_link_flag = params[6]
        self.cost_qty_type = params[7]
        self.role_descr = params[8]
        self.last_checksum = params[9]

        Role.obj_list.append(self)

    def __repr__(self):
        return self.role_name
