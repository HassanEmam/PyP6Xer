from xerparser.model.classes.acttype import ActType

class ActTypes:

    _activitytypes = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._activitytypes.append(ActType(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._activitytypes))
        if len(obj) > 0:
            return obj[0]
        return obj


    @staticmethod
    def count():
        return len(ActTypes._activitytypes)

    def __len__(self):
        return len(ActTypes._activitytypes)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._activitytypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitytypes[idx]