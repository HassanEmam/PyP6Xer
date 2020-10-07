from xerparser.model.classes.taskrsrc import TaskRsrc
from xerparser.model.classes.rsrc import Resource

class ActivityResources:

    _taskrsrc = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._taskrsrc.append(TaskRsrc(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.taskrsrc_id == id , cls._taskrsrc))
        if len(obj) > 0:
            return obj[0]
        return obj

    @classmethod
    def find_by_activity_id(cls, id):
        obj = list(filter(lambda x: x.task_id == id and x.rsrc_id, cls._taskrsrc))
        obj1 = [{Resource.find_by_id(x.rsrc_id): {"BL_QTY":x.target_qty, "ACT_QTY": x.act_reg_qty,\
                                                  "REM_QTY": x.remain_qty}} for x in obj]
        return obj1

    @property
    def count(self):
        return len(self._taskrsrc)

    def __len__(self):
        return len(ActivityResources._taskrsrc)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._taskrsrc):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._taskrsrc[idx]