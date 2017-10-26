class ResourceRate:
    rsrc_rate_id = None
    rsrc_id = None
    max_qty_per_hr = None
    cost_per_qty = None
    start_date = None
    shift_period_id = None
    cost_per_qty2 = None
    cost_per_qty3 = None
    cost_per_qty4 = None
    cost_per_qty5 = None

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

    def get_id(self):
        return self.rsrc_rate_id

    @staticmethod
    def find_by_resource_id(resource_id, resources_dict):
        return {k: v for k, v in resources_dict.items() if v.rsrc_id == resource_id}

    def __repr__(self):
        return self.rsrc_id
