from xerparser.model.classes.rsrcrcat import ResourceCat

class ResourceCategories:

    _rsrccat = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._rsrccat.append(ResourceCat(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._rsrccat))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rsrccat)

    def __len__(self):
        return len(ResourceCategories._rsrccat)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._rsrccat):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrccat[idx]