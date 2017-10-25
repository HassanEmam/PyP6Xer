class ResourceRate:
    rsrc_rate_id = ''
    rsrc_id = ''
    max_qty_per_hr = ''
    cost_per_qty = ''
    start_date = ''
    shift_period_id = ''
    cost_per_qty2 = ''
    cost_per_qty3 = ''
    cost_per_qty4 = ''
    cost_per_qty5 = ''

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
