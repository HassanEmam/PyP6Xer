from xerparser.model.classes.project import Project

class Projects:
    _projects = []

    def __init__(self):
        self.index =0

    def add(self, params):
        prj = Project(params)
        self._projects.append(prj)

    def find_by_id(self, id):
        obj = list(filter(lambda x: x.proj_id == id, Project.obj_list))
        if obj:
            return obj[0]
        return obj

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._projects):
            raise StopIteration
        idx = self.index
        self.index +=1
        return self._projects[idx]