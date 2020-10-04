class TaskActv:
    obj_list = []

    def __init__(self, params):
        self.task_id = int(params[0].strip()) if params[0].strip() else None
        self.actv_code_type_id = params[1].strip()
        self.actv_code_id = int(params[2].strip()) if params[2].strip() else None
        self.proj_id = int(params[3].strip()) if params[3].strip() else None

        TaskActv.obj_list.append(self)

    def get_id(self):
        return self.task_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.task_id + '->' + self.actv_code_id