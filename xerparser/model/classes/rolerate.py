

class RoleRate:
    obj_list = []

    def __init__(self, params):
        self.role_rate_id = int(params[0]) if params[0] else None
        self.role_id = int(params[1]) if params[1] else None
        self.cost_per_qty = float(params[2]) if params[2] else None
        self.cost_per_qty2 = float(params[3])if params[3] else None
        self.cost_per_qty3 = float(params[4]) if params[4] else None
        self.cost_per_qty4 = float(params[5]) if params[5] else None
        self.cost_per_qty5 = None if params[6] == '\n' or params[6] == '' else float(params[6])

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
