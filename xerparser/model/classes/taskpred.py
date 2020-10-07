class TaskPred:

    obj_list = []

    def __init__(self, params):
        self.task_pred_id = params.get('task_pred_id').strip() if params.get('task_pred_id') else None
        self.task_id = int(params.get('task_id')) if params.get('task_id') else None
        self.pred_task_id = int(params.get('pred_task_id')) if params.get('pred_task_id') else None
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.pred_proj_id = params.get('proj_id').strip() if params.get('pred_proj_id') else None
        self.pred_type = params.get('pred_type').strip() if params.get('pred_type') else None
        self.lag_hr_cnt = params.get('lag_hr_cnt').strip() if params.get('lag_hr_cnt') else None
        self.float_path = params.get('float_path').strip() if params.get('float_path') else None
        self.aref = params.get('aref').strip() if params.get('aref') else None
        self.arls = params.get('arls').strip() if params.get('arls') else None
        TaskPred.obj_list.append(self)

    def get_id(self):
        return self.task_pred_id



    def __repr__(self):
        return str(self.task_id) + '->' + str(self.pred_task_id)