class ActivityCode:

    actv_code_id = ''
    parent_actv_code_id = ''
    actv_code_type_id = ''
    actv_code_name = ''
    short_name = ''
    seq_num = ''
    color = ''
    total_assignments = ''

    def __init__(self, params):
        self.actv_code_id = params[0].strip()
        self.parent_actv_code_id = params[1].strip()
        self.actv_code_type_id = params[2].strip()
        self.actv_code_name = params[3].strip()
        self.short_name = params[4].strip()
        self.seq_num = params[5].strip()
        self.color = params[6].strip()
        self.total_assignments = params[7].strip()

    def get_id(self):
        return self.actv_code_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.actv_code_name