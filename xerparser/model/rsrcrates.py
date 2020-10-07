from xerparser.model.classes.rsrcrate import ResourceRate

class ResourceRates:

    _rsrcrates = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._rsrcrates.append(ResourceRate(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._rsrcrates))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rsrcrates)

    def __len__(self):
        return len(ResourceRates._rsrcrates)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._rsrcrates):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrcrates[idx]