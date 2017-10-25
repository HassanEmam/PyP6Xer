class ActType:
    actv_code_type_id = ''
    actv_short_len = ''
    seq_num = ''
    actv_code_type = ''
    proj_id = ''
    wbs_id = ''
    actv_code_type_scope = ''

    def __init__(self, params):
        self.actv_code_type_id = params[0].strip()
        self.actv_short_len = params[1].strip()
        self.seq_num = params[2].strip()
        self.actv_code_type = params[3].strip()
        self.proj_id = params[4].strip()
        self.wbs_id = params[5].strip()
        self.actv_code_type_scope = params[6].strip()

    def get_id(self):
        return self.actv_code_type_id

    def __repr__(self):
        return self.actv_code_type

