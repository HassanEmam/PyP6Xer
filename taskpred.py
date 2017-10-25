class TaskPred:
    task_pred_id = ''
    task_id = ''
    pred_task_id = ''
    proj_id = ''
    pred_proj_id = ''
    pred_type = ''
    lag_hr_cnt = ''
    float_path = ''
    aref = ''
    arls = ''

    def __init__(self, params):
        self.task_pred_id = params[0].strip()
        self.task_id = params[1].strip()
        self.pred_task_id = params[2].strip()
        self.proj_id = params[3].strip()
        self.pred_proj_id = params[4].strip()
        self.pred_type = params[5].strip()
        self.lag_hr_cnt = params[6].strip()
        self.float_path = params[7].strip()
        self.aref = params[8].strip()
        self.arls = params[9].strip()

    def get_id(self):
        return self.task_pred_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.task_id + '->' + self.pred_task_id