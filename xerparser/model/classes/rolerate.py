

class RoleRate:
    obj_list = []

    def __init__(self, params):
        self.role_rate_id = int(params.get('role_rate_id').strip()) if params.get('role_rate_id') else None
        self.role_id = int(params.get('role_id').strip()) if params.get('role_id') else None
        self.cost_per_qty = float(params.get('cost_per_qty').strip()) if params.get('cost_per_qty') else None
        self.cost_per_qty2 = float(params.get('cost_per_qty2').strip())if params.get('cost_per_qty2') else None
        self.cost_per_qty3 = float(params.get('cost_per_qty3').strip()) if params.get('cost_per_qty3') else None
        self.cost_per_qty4 = float(params.get('cost_per_qty4').strip()) if params.get('cost_per_qty4') else None
        self.cost_per_qty5 = float(params.get('cost_per_qty5').strip()) if params.get('cost_per_qty5') else None

        RoleRate.obj_list.append(self)

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.role_rate_id == id, cls.obj_list))[0]
        return obj

    @classmethod
    def find_by_role_id(cls, id):
        obj = list(filter(lambda x: x.role_id == id, cls.obj_list))
        if len(obj) > 0:
            obj = obj[0]
        else:
            obj = None
        return obj

    def __repr__(self):
        return str(self.role_rate_id)
