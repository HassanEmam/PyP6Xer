from xerparser.model.classes.currency import Currency

class Currencies:



    def __init__(self):
        self.index = 0
        self._currencies = []

    def add(self, params):
        self._currencies.append(Currency(params))

    def find_by_id(self, id) -> Currency:
        obj = list(filter(lambda x: x.curr_id == id, self._currencies))
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