from xerparser.model.classes.taskactv import TaskActv


class TaskActvs:

    def __init__(self):
        self.index = 0
        self._taskactvs = []

    def add(self, params):
        self._taskactvs.append(TaskActv(params))
    
    def get_tsv(self):
        tsv = []
        if len(self._taskactvs) > 0:
            tsv.append(['%T', 'TASKACTV'])
            tsv.append(['%F', 'task_id', 'actv_code_type_id', 'actv_code_id', 'proj_id'])
            for taskact in self._taskactvs:
                tsv.append(taskact.get_tsv())
        return tsv
    
    def find_by_code_id(self, id) -> TaskActv:
        obj = list(filter(lambda x: x.actv_code_id == id, self._taskactvs))
        if len(obj) > 0:
            return obj
        return obj

    def find_by_activity_id(self, id) -> TaskActv:
        obj = list(filter(lambda x: x.task_id == id, self._taskactvs))
        if len(obj) > 0:
            return obj
        return obj

    def count(self):
        return len(self._taskactvs)

    def __len__(self):
        return len(self._taskactvs)

    def __iter__(self):
        return self

    def __next__(self) -> TaskActv:
        if self.index >= len(self._taskactvs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._taskactvs[idx]