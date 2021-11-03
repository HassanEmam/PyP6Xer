

class RCatVal:
    obj_list = []

    def __init__(self, params):
        self.rsrc_catg_id = params.get('rsrc_catg_id').strip() if params.get('rsrc_catg_id') else None
        self.rsrc_catg_type_id = params.get('rsrc_catg_type_id').strip() if params.get('rsrc_catg_type_id') else None
        self.rsrc_catg_short_name = params.get('rsrc_catg_short_name').strip() if params.get('rsrc_catg_short_name') else None
        self.rsrc_catg_name = params.get('rsrc_catg_name').strip() if params.get('rsrc_catg_name') else None
        self.parent_rsrc_catg_id = params.get('parent_rsrc_catg_id').strip() if params.get('parent_rsrc_catg_id') else None
        RCatVal.obj_list.append(self)

    def get_id(self):
        return self.rsrc_catg_id

    def get_tsv(self):
        tsv = ['%R', self.rsrc_catg_id, self.rsrc_catg_type_id, self.rsrc_catg_short_name,
               self.rsrc_catg_name, self.parent_rsrc_catg_id]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.rsrc_catg_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.rsrc_catg_name