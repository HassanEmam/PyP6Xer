class ActType:
    obj_list =[]

    def __init__(self, params):
        self.actv_code_type_id = params[0].strip()
        self.actv_short_len = params[1].strip()
        self.seq_num = params[2].strip()
        self.actv_code_type = params[3].strip()
        self.proj_id = params[4].strip()
        self.wbs_id = params[5].strip()
        self.actv_code_type_scope = params[6].strip()
        ActType.obj_list.append(self)
    def get_id(self):
        return self.actv_code_type_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.actv_code_type

