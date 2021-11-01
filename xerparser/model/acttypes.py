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