from xerparser.model.classes.rcatval import RCatVal

class RCatVals:

    _rcatvals = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._rcatvals.append(RCatVal(params))

    @classmethod
    def find_by_id(cls, id) -> RCatVal:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._rcatvals))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rcatvals)

    def __len__(self):
        return len(RCatVals._rcatvals)

    def __iter__(self):
        return self

    def __next__(self) -> RCatVal:
        if self.index >= len(self._rcatvals):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rcatvals[idx]