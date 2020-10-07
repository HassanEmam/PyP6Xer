from xerparser.model.classes.calendar import Calendar


class Calendars:
    _calendars = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._calendars.append(Calendar(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._calendars))
        if len(obj) > 0:
            return obj[0]
        return obj

    @staticmethod
    def count():
        return len(Calendar._calendars)

    def __len__(self):
        return len(Calendar._calendars)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._activitytypes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitytypes[idx]