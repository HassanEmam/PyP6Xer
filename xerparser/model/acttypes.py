from xerparser.model.classes.acttype import ActType

class ActTypes:



    def __init__(self):
        self.index = 0
        self._activitytypes = []

    def add(self, params):
        self._activitytypes.append(ActType(params))

    def find_by_id(self, id) -> ActType:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._activitytypes))
        if len(obj) > 0:
            return obj[0]
        return obj

    def get_tsv(self):
        if len(self._activitytypes) > 0:
            tsv = []
            tsv.append(['%T', 'ACTVTYPE'])
            tsv.append(['%f', 'actv_code_type_id', 'actv_short_len', 'seq_num',
                        'actv_code_type', 'proj_id', 'wbs_id', 'actv_code_type_scope'])
            for acttyp in self._activitytypes:
                tsv.append(acttyp.get_tsv())
            return tsv
        return []

    def count(self):
        return len(self._activitytypes)

    def __len__(self):
        return len(self._activitytypes)

    def __iter__(self):
        return self

    def __next__(self) -> ActType:
        if self.index >= len(self._activitytypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitytypes[idx]