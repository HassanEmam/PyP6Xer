class TaskPred:

    obj_list = []

    def __init__(self, params):
        self.task_pred_id = params.get('task_pred_id').strip() if params.get('task_pred_id') else None
        self.task_id = int(params.get('task_id')) if params.get('task_id') else None
        self.pred_task_id = int(params.get('pred_task_id')) if params.get('pred_task_id') else None
        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None
        self.pred_proj_id = int(params.get('proj_id').strip()) if params.get('pred_proj_id') else None
        self.pred_type = params.get('pred_type').strip() if params.get('pred_type') else None
        self.lag_hr_cnt = int(params.get('lag_hr_cnt').strip()) if params.get('lag_hr_cnt') else None
        self.float_path = params.get('float_path').strip() if params.get('float_path') else None
        self.aref = params.get('aref').strip() if params.get('aref') else None
        self.arls = params.get('arls').strip() if params.get('arls') else None
        self.comments = params.get('comments').strip() if params.get('comments') else None
        TaskPred.obj_list.append(self)

    def get_id(self):
        return self.task_pred_id

    def get_tsv(self):
        tsv = ['%R', self.task_pred_id, self.task_id, self.pred_task_id, self.proj_id, self.pred_proj_id,
               self.pred_type, self.lag_hr_cnt, self.comments, self.float_path, self.aref, self.arls]
        return tsv
    def __repr__(self):
        return str(self.task_id) + '- ' + self.pred_type + ' ->' + str(self.pred_task_id) + ' lag: ' + str(self.lag_hr_cnt)