
class RCatType:
    rsrc_catg_type_id = ''
    seq_num = ''
    rsrc_catg_short_len = ''
    rsrc_catg_type = ''

    def __init__(self, params):
        self.rsrc_catg_type_id = params[0].strip()
        self.seq_num = params[1].strip()
        self.rsrc_catg_short_len = params[2].strip()
        self.rsrc_catg_type = params[3].strip()

    def get_id(self):
        return self.rsrc_catg_type_id

    def __repr__(self):
        return self.rsrc_catg_type