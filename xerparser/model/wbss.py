from xerparser.model.classes.wbs import WBS
from typing import List


class WBSs:

    def __init__(self):
        self.index = 0
        self._wbss = []

    def add(self, params):
        wbs = WBS(params)
        self._wbss.append(wbs)

    def get_by_project(self, id) -> List[WBS]:
        return list(filter(lambda x: x.proj_id == id, self._wbss))

    def __iter__(self):
        return self

    def __next__(self) -> WBS:
        if self.index >= len(self._wbss):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._wbss[idx]
