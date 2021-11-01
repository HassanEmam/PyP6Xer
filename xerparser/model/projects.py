from xerparser.model.classes.project import Project

class Projects:


    def __init__(self):
        self.index =0
        self._projects = []

    def add(self, params):
        prj = Project(params)
        self._projects.append(prj)

    def find_by_id(self, id) -> Project:
        obj = list(filter(lambda x: x.proj_id == id, self._projects))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return str(self._projects)

    def __iter__(self):
        return self

    def __next__(self) -> Project:
        if self.index >= len(self._projects):
            raise StopIteration
        idx = self.index
        self.index +=1
        return self._projects[idx]