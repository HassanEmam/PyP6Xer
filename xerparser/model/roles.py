from xerparser.model.classes.role import Role


class Roles:

    def __init__(self):
        self.index = 0
        self._roles = []

    def get_tsv(self):
        if len(self._roles) > 0:
            tsv = []
            tsv.append(['%T', 'ROLE'])
            tsv.append(['%F', 'role_id', 'parent_role_id', 'seq_num', 'role_name',
                   'role_short_name', 'pobs_id', 'def_cost_qty_link_flag', 'cost_qty_type',
                   'role_descr', 'last_checksum'])
            for role in self._roles:
                tsv.append(role.get_tsv())
            return tsv
        return []

    def add(self, params):
        self._roles.append(Role(params))

    def find_by_id(self, id) -> Role:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._roles))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._roles)

    def __len__(self):
        return len(self._roles)

    def __iter__(self):
        return self

    def __next__(self) -> Role:
        if self.index >= len(self._roles):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._roles[idx]