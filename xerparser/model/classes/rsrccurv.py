

class ResourceCurve:
    obj_list = []

    def __init__(self, params):
        self.curv_id = int(params[0]) if params[0] else None
        self.curv_name = params[1].strip()
        self.default_flag = params[2]
        self.pct_usage_0 = float(params[3]) if params[3] else None
        self.pct_usage_1 = float(params[4]) if params[4] else None
        self.pct_usage_2 = float(params[5]) if params[5] else None
        self.pct_usage_3 = float(params[6]) if params[6] else None
        self.pct_usage_4 = float(params[7]) if params[7] else None
        self.pct_usage_5 = float(params[8]) if params[8] else None
        self.pct_usage_6 = float(params[9]) if params[9] else None
        self.pct_usage_7 = float(params[10]) if params[10] else None
        self.pct_usage_8 = float(params[11]) if params[11] else None
        self.pct_usage_9 = float(params[12]) if params[12] else None
        self.pct_usage_10 = float(params[13]) if params[13] else None
        self.pct_usage_11 = float(params[14]) if params[14] else None
        self.pct_usage_12 = float(params[15]) if params[15] else None
        self.pct_usage_13 = float(params[16]) if params[16] else None
        self.pct_usage_14 = float(params[17]) if params[17] else None
        self.pct_usage_15 = float(params[18]) if params[18] else None
        self.pct_usage_16 = float(params[19]) if params[19] else None
        self.pct_usage_17 = float(params[20]) if params[20] else None
        self.pct_usage_18 = float(params[21]) if params[21] else None
        self.pct_usage_19 = float(params[22]) if params[22] else None
        self.pct_usage_20 = float(params[23]) if params[23] else None

        ResourceCurve.obj_list.append(self)

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.curv_id == id, cls.obj_list))[0]
        return obj

    def __repr__(self):
        return self.curv_name
