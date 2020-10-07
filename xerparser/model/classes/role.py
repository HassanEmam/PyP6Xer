

class Role:
    obj_list = []

    def __init__(self, params):
        self.role_id = int(params.get('role_id')) if params.get('role_id') else None
        self.parent_role_id = int(params.get('parent_role_id')) if params.get('parent_role_id') else None
        self.seq_num = int(params.get('seq_num')) if params.get('seq_num') else None
        self.role_name = params.get('role_name') if params.get('role_name') else None
        self.role_short_name = params.get('role_short_name') if params.get('role_short_name') else None
        self.pobs_id = params.get('pobs_id') if params.get('pobs_id') else None
        self.def_cost_qty_link_flag = params.get('def_cost_qty_link_flag') if params.get('def_cost_qty_link_flag') else None
        self.cost_qty_type = params.get('cost_qty_type') if params.get('cost_qty_type') else None
        self.role_descr = params.get('role_descr') if params.get('role_descr') else None
        self.last_checksum = params.get('role_descr') if params.get('role_descr') else None

        Role.obj_list.append(self)

    def __repr__(self):
        return self.role_name
