class TaskActv:
    task_id = None
    actv_code_type_id = None
    actv_code_id = None
    proj_id = None

    def __init__(self, params):
        self.task_id = params[0].strip()
        self.actv_code_type_id = params[1].strip()
        self.actv_code_id = params[2].strip()
        self.proj_id = params[3].strip()

    def get_id(self):
        return self.task_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.task_id + '->' + self.actv_code_id