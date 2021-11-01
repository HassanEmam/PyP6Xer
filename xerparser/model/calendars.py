from xerparser.model.classes.calendar import Calendar


class Calendars:


    def __init__(self):
        self.index = 0
        self._calendars = []

    def add(self, params):
        self._calendars.append(Calendar(params))

    def find_by_id(self, id) -> Calendar:
        obj = list(filter(lambda x: x.clndr_id == id, self._calendars))
        if len(obj) > 0:
            return obj[0]
        return obj

    def count(self):
        return len(self._calendars)

    def __len__(self):
        return len(self._calendars)

    def __iter__(self):
        return self

    def __next__(self) -> Calendar:
        if self.index >= len(self._calendars):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._calendars[idx]