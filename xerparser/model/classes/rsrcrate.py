class ResourceRate:
    obj_list = []

    def __init__(self, params):
        self.rsrc_rate_id = params[0].strip()
        self.rsrc_id = params[1].strip()
        self.max_qty_per_hr = params[2].strip()
        self.cost_per_qty = params[3].strip()
        self.start_date = params[4].strip()
        self.shift_period_id = params[5].strip()
        self.cost_per_qty2 = params[6].strip()
        self.cost_per_qty3 = params[7].strip()
        self.cost_per_qty4 = params[8].strip()
        self.cost_per_qty5 = params[9].strip()
        ResourceRate.obj_list.append(self)

    def get_id(self):
        return self.rsrc_rate_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_rate_id == id, cls.obj_list))
        if len(obj) > 0:
            obj = obj[0]
        else:
            None
        return obj

    @classmethod
    def find_by_resource_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_rate_id == id, cls.obj_list))
        if len(obj) > 0:
            obj = obj[0]
        else:
            obj = None
        return obj

    def __repr__(self):
        return self.rsrc_id
