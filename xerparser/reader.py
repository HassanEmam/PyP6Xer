'''
This file starts the process of reading and parsing xer files

'''
from xerparser import *


class Reader:

    current_table = ''
    currencies = []
    obs = []

    project = []
    calendar = []
    wbs = []
    resource = []

    task = []

    def create_object(self, object_type, params):
        """

        Args:
            object_type:
            params:

        Returns:

        """
        if object_type.strip() == "CURRTYPE":
            obj = Currency(params)
            return obj
        elif object_type.strip() == "ROLES":
            obj = Role(params)
            return obj
        elif object_type.strip() == "ACCOUNT":
            obj = Account(params)
            return obj
        elif object_type.strip() == "ROLERATE":
            obj = RoleRate(params)
            return obj
        elif object_type.strip() == "OBS":
            obj = OBS(params)
            return obj
        elif object_type.strip() == "RCATTYPE":
            obj = RCatType(params)
            return obj
        elif object_type.strip() == "UDFTYPE":
            obj = UDFType(params)
            return obj
        elif object_type.strip() == "RCATVAL":
            obj = RCatVal(params)
            return obj
        elif object_type.strip() == "PROJECT":
            obj = Project(params)
            return obj
        elif object_type.strip() == "CALENDAR":
            obj = Calendar(params)
            # print(params)
            return obj
        elif object_type.strip() == "SCHEDOPTIONS":
            obj = SchedOption(params)
            return obj
        elif object_type.strip() == "PROJWBS":
            obj = WBS(params)
            # self.wbs.append(obj)
            return obj
        elif object_type.strip() == "RSRC":
            obj = Resource(params)
            return obj
        elif object_type.strip() == "ACTVTYPE":
            obj = ActType(params)
            return obj
        elif object_type.strip() == "RSRCRATE":
            obj = ResourceRate(params)
            return obj
        elif object_type.strip() == "RSRCRCAT":
            obj = ResourceCat(params)
            return obj
        elif object_type.strip() == "TASK":
            self.tasks.add_task(params)
            #self.task.append(obj)
            # return obj
        elif object_type.strip() == "ACTVCODE":
            obj = ActivityCode(params)
            return obj
        elif object_type.strip() == "TASKPRED":
            obj = TaskPred(params)
            return obj
        elif object_type.strip() == "TASKRSRC":
            obj = TaskRsrc(params)
            return obj
        elif object_type.strip() == "TASKACTV":
            obj = TaskActv(params)
            return obj
        elif object_type.strip() == "UDFVALUE":
            obj = UDFValue(params)
            return obj

    def summary(self):
        print('Number of activities: ', self.tasks.count)
        print('Number of relationships: ', len(TaskPred.obj_list))

    def __init__(self, filename):
        file = open(filename, 'r')
        self.tasks = Tasks()
        content = file.readlines()
        for line in content:
            line_lst = line.split('\t')
            if line_lst[0] == "%T":
                current_table = line_lst[1]
            elif line_lst[0] == "%R":
                self.create_object(current_table, line_lst[1:])


