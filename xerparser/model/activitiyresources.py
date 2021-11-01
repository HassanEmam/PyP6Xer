from xerparser.model.classes.taskrsrc import TaskRsrc
from xerparser.model.classes.rsrc import Resource


class ActivityResources:

    def __init__(self):
        self.index = 0
        self._taskrsrc = []

    def add(self, params):
        self._taskrsrc.append(TaskRsrc(params))

    def find_by_id(self, id) -> TaskRsrc:
        obj = list(filter(lambda x: x.taskrsrc_id == id, self._taskrsrc))
        if len(obj) > 0:
            return obj[0]
        return None

    def find_by_rsrc_id(self, id) -> TaskRsrc:
        obj = list(filter(lambda x: x.rsrc_id == id, self._taskrsrc))
        return obj

    def find_by_activity_id(self, id):
        obj = list(filter(lambda x: x.task_id == id and x.rsrc_id, self._taskrsrc))
        return obj

    @property
    def count(self):
        return len(self._taskrsrc)

    def __len__(self):
        return len(ActivityResources._taskrsrc)

    def __iter__(self):
        return self

    def __next__(self) -> TaskRsrc:
        if self.index >= len(self._taskrsrc):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._taskrsrc[idx]