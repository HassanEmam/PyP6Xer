class TaskPred:

    obj_list = []

    def __init__(self, params):
        self.task_pred_id = params[0].strip()
        self.task_id = int(params[1]) if params[1] else None
        self.pred_task_id = int(params[2]) if params[2] else None
        self.proj_id = params[3].strip()
        self.pred_proj_id = params[4].strip()
        self.pred_type = params[5].strip()
        self.lag_hr_cnt = params[6].strip()
        self.float_path = params[7].strip()
        self.aref = params[8].strip()
        self.arls = params[9].strip()
        TaskPred.obj_list.append(self)

    def get_id(self):
        return self.task_pred_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.task_id + '->' + self.pred_task_id