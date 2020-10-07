from xerparser.model.classes.activitycode import ActivityCode

class ActivityCodes:

    _activitycodes = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._activitycodes.append(ActivityCode(params))

    @staticmethod
    def count():
        return len(ActivityCodes._activitycodes)

    def __len__(self):
        return len(ActivityCodes._activitycodes)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._activitycodes):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._activitycodes[idx]