
class RCatType:
    obj_list = []

    def __init__(self, params):
        self.rsrc_catg_type_id = int(params.get('rsrc_catg_type_id').strip()) if params.get('rsrc_catg_type_id') else None
        self.seq_num = params.get('seq_num').strip() if params.get('seq_num') else None
        self.rsrc_catg_short_len = params.get('rsrc_catg_short_len').strip() if params.get('rsrc_catg_short_len') else None
        self.rsrc_catg_type = params.get('rsrc_catg_type').strip() if params.get('rsrc_catg_type') else None
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