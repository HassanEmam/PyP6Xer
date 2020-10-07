from xerparser.model.classes.rsrccurv import ResourceCurve

class ResourceCurves:

    _resourcecurves = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._resourcecurves.append(ResourceCurve(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._resourcecurves))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._resourcecurves)

    def __len__(self):
        return len(ResourceCurves._resourcecurves)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._resourcecurves):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._resourcecurves[idx]