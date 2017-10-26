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
        self.seq_num = int(params[5]) if params[5] else None
        self.color = params[6].strip()
        self.total_assignments = int(params[7]) if params[7] else None

    def get_id(self):
        return self.actv_code_id

    @classmethod
    def find_by_id(cls, code_id, activity_code_list):
        actv_code = list(filter(lambda x: x.actv_code_id == code_id, activity_code_list))[0]
        obj = cls([actv_code.actv_code_id, actv_code.parent_actv_code_id, actv_code.actv_code_type_id,
                   actv_code.actv_code_name, actv_code.short_name, actv_code.seq_num, actv_code.color,
                   actv_code.total_assignments])
        return obj

    @classmethod
    def find_by_code(cls, code, activity_code_list):
        actv_code = list(filter(lambda x: x.short_name == code, activity_code_list))[0]
        obj = cls([actv_code.actv_code_id, actv_code.parent_actv_code_id, actv_code.actv_code_type_id,
                   actv_code.actv_code_name, actv_code.short_name, actv_code.seq_num, actv_code.color,
                   actv_code.total_assignments])
        return obj

    def __repr__(self):
        return self.actv_code_id + ' - ' + self.short_name + ' - ' + self.actv_code_name
