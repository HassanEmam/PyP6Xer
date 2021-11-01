from xerparser.model.classes.rsrcrcat import ResourceCat


class ResourceCategories:

    def __init__(self):
        self.index = 0
        self._rsrccat = []

    def add(self, params):
        self._rsrccat.append(ResourceCat(params))

    def find_by_id(self, id) -> ResourceCat:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rsrccat))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rsrccat)

    def __len__(self):
        return len(self._rsrccat)

    def __iter__(self):
        return self

    def __next__(self) -> ResourceCat:
        if self.index >= len(self._rsrccat):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrccat[idx]
