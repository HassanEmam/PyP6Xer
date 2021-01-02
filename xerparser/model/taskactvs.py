from xerparser.model.classes.taskactv import TaskActv


class TaskActvs:
    _taskactvs = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._taskactvs.append(TaskActv(params))

    @classmethod
    def find_by_code_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_id == id, cls._taskactvs))
        if len(obj) > 0:
            return obj
        return obj

    @classmethod
    def find_by_activity_id(cls, id):
        obj = list(filter(lambda x: x.task_id == id, cls._taskactvs))
        if len(obj) > 0:
            return obj
        return obj

    @staticmethod
    def count():
        return len(TaskActvs._taskactvs)

    def __len__(self):
        return len(self._taskactvs)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._taskactvs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._taskactvs[idx]