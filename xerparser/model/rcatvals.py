from xerparser.model.classes.rcatval import RCatVal

class RCatVals:



    def __init__(self):
        self.index = 0
        self._rcatvals = []

    def add(self, params):
        self._rcatvals.append(RCatVal(params))
    
    def get_tsv(self):
        if len(self._rcatvals) > 0:
            tsv = []
            tsv.append(['%T', 'RCATVAL'])
            tsv.append(['%F', 'rsrc_catg_id', 'rsrc_catg_type_id', 'rsrc_catg_short_name',
                        'rsrc_catg_name', 'parent_rsrc_catg_id'])
            for rc in self._rcatvals:
                tsv.append(rc.get_tsv())
            return tsv
        return []
    
    def find_by_id(self, id) -> RCatVal:
        obj = list(filter(lambda x: x.actv_code_type_id == id, self._rcatvals))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._rcatvals)

    def __len__(self):
        return len(self._rcatvals)

    def __iter__(self):
        return self

    def __next__(self) -> RCatVal:
        if self.index >= len(self._rcatvals):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rcatvals[idx]
