class TaskActv:
    obj_list = []

    def __init__(self, params):
        self.task_id = int(params.get('task_id').strip()) if params.get('task_id') else None
        self.actv_code_type_id = params.get('actv_code_type_id').strip()
        self.actv_code_id = int(params.get('actv_code_id').strip()) if params.get('actv_code_id') else None
        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None

        TaskActv.obj_list.append(self)

    def get_id(self):
        return self.task_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return str(self.task_id) + '->' + str(self.actv_code_id)