

class RCatVal:
    rsrc_catg_id = ''
    rsrc_catg_type_id = ''
    seq_num = ''
    rsrc_catg_short_name = ''
    rsrc_catg_name = ''
    parent_rsrc_catg_id = ''

    def __init__(self, params):
        self.rsrc_catg_id = params[0].strip()
        self.rsrc_catg_type_id = params[1].strip()
        self.rsrc_catg_short_name = params[2].strip()
        self.rsrc_catg_name = params[3].strip()
        self.parent_rsrc_catg_id = params[4].strip()

    def get_id(self):
        return self.rsrc_catg_id

    def __repr__(self):
        return self.rsrc_catg_name