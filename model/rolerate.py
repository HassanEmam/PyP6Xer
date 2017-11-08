

class RoleRate:
    obj_list = []

    def __init__(self, params):
        self.role_rate_id = params[0]
        self.role_id = params[1]
        self.cost_per_qty = params[2]
        self.cost_per_qty2 = params[3]
        self.cost_per_qty3 = params[4]
        self.cost_per_qty4 = params[5]
        self.cost_per_qty5 = params[6]


        RoleRate.obj_list.append(self)

    def __repr__(self):
        return self.role_name
