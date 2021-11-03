from xerparser.model.classes.rolerate import RoleRate


class RoleRates:

    def __init__(self):
        self.index = 0
        self._rolerates = []

    def get_tsv(self):
        tsv = []
        if len(self._rolerates) > 0:
            tsv.append(['%T', 'ROLERATE'])
            tsv.append(['%F', 'role_rate_id', 'role_id', 'cost_per_qty', 'cost_per_qty2',
                   'cost_per_qty3', 'cost_per_qty4', 'cost_per_qty5'])
            for rr in self._rolerates:
                tsv.append(rr.get_tsv())
        return tsv

    def add(self, params):
        self._rolerates.append(RoleRate(params))
        self._rolerates = []

    def find_by_id(self, id) -> RoleRate:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rolerates))
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