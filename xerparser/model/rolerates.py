from xerparser.model.classes.rolerate import RoleRate

class RoleRates:

    _rolerates = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._rolerates.append(RoleRate(params))

    @classmethod
    def find_by_id(cls, id) -> RoleRate:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._rolerates))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rolerates)

    def __len__(self):
        return len(self._rolerates)

    def __iter__(self):
        return self

    def __next__(self) -> RoleRate:
        if self.index >= len(self._rolerates):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rolerates[idx]