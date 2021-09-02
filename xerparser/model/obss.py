from xerparser.model.classes.obs import OBS

class OBSs:

    _obss = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._obss.append(OBS(params))

    @classmethod
    def find_by_id(cls, id) -> OBS:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._obss))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._obss)

    def __len__(self):
        return len(OBSs._obss)

    def __iter__(self):
        return self

    def __next__(self) -> OBS:
        if self.index >= len(self._obss):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._obss[idx]