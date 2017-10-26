
class RCatType:
    obj_list = []

    def __init__(self, params):
        self.rsrc_catg_type_id = params[0].strip()
        self.seq_num = params[1].strip()
        self.rsrc_catg_short_len = params[2].strip()
        self.rsrc_catg_type = params[3].strip()
        RCatType.obj_list.append(self)

    def get_id(self):
        return self.rsrc_catg_type_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_catg_type_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.rsrc_catg_type