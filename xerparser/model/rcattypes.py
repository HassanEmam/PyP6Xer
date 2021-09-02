from xerparser.model.classes.rcattype import RCatType

class RCatTypes:

    _rcattypes = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._rcattypes.append(RCatType(params))

    @classmethod
    def find_by_id(cls, id) -> RCatType:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._rcattypes))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rcattypes)

    def __len__(self):
        return len(RCatTypes._rcattypes)

    def __iter__(self):
        return self

    def __next__(self) -> RCatType:
        if self.index >= len(self._rcattypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rcattypes[idx]