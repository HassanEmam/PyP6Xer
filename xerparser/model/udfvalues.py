from xerparser.model.classes.udfvalue import UDFValue

class UDFValues:

    _udfvalues = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._udfvalues.append(UDFValue(params))

    @classmethod
    def find_by_id(cls, id) -> UDFValue:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._udfvalues))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._udfvalues)

    def __len__(self):
        return len(self._udfvalues)

    def __iter__(self):
        return self

    def __next__(self) -> UDFValue:
        if self.index >= len(self._udfvalues):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._udfvalues[idx]