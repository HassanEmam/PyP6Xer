from xerparser.model.classes.currency import Currency

class Currencies:

    _currencies = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._currencies.append(Currency(params))

    @classmethod
    def find_by_id(cls, id) -> Currency:
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._currencies))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._currencies)

    def __len__(self):
        return len(self._currencies)

    def __iter__(self):
        return self

    def __next__(self) -> Currency:
        if self.index >= len(self._currencies):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._currencies[idx]