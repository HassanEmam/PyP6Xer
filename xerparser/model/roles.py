from xerparser.model.classes.role import Role


class Roles:

    _roles = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._roles.append(Role(params))

    @classmethod
    def find_by_id(cls, id) -> Role:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._roles))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._roles)

    def __len__(self):
        return len(Roles._roles)

    def __iter__(self):
        return self

    def __next__(self) -> Role:
        if self.index >= len(self._roles):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._roles[idx]