'''
This file starts the process of reading and parsing xer files

'''

from model.calendar import Calendar
from model.activitycode import ActivityCode
from model.acttype import ActType
from model.obs import OBS
from model.project import Project
from model.rcattype import RCatType
from model.rcatval import RCatVal
from model.rsrc import Resource
from model.rsrcrate import ResourceRate
from model.rsrcrcat import ResourceCat
from model.schedoption import SchedOption
from model.task import Task
from model.taskactv import TaskActv
from model.taskpred import TaskPred
from model.udftypes import UDFType
from model.udfvalue import UDFValue
from model.wbs import WBS
from model.currency import Currency
from model.taskrsrc import TaskRsrc


class Reader:

    current_table = ''
    currencies = dict()
    obs = dict()
    rcattype = dict()
    udftype = dict()
    rcatval = dict()
    project = dict()
    calendar = dict()
    schedoption = dict()
    wbs = dict()
    resource = dict()
    acttype = dict()
    rsrcrate = dict()
    rsrcrcat = dict()
    task = dict()
    actvcode = dict()
    taskpred = dict()
    taskrsrc = dict()
    taskactv = dict()
    udfvalue = dict()

    def create_object(self, object_type, params):
        if object_type.strip() == "CURRTYPE":
            obj = Currency(params)
            self.currencies[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "OBS":
            obj = OBS(params)
            self.obs[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "RCATTYPE":
            obj = RCatType(params)
            self.rcattype[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "UDFTYPE":
            obj = UDFType(params)
            self.udftype[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "RCATVAL":
            obj = RCatVal(params)
            self.rcatval[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "PROJECT":
            obj = Project(params)
            self.project[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "CALENDAR":
            obj = Calendar(params)
            self.calendar[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "SCHEDOPTIONS":
            obj = SchedOption(params)
            self.schedoption[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "PROJWBS":
            obj = WBS(params)
            self.wbs[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "RSRC":
            obj = Resource(params)
            self.resource[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "ACTVTYPE":
            obj = ActType(params)
            self.acttype[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "RSRCRATE":
            obj = ResourceRate(params)
            self.rsrcrate[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "RSRCRCAT":
            obj = ResourceCat(params)
            self.rsrcrcat[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "TASK":
            obj = Task(params)
            self.task[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "ACTVCODE":
            obj = ActivityCode(params)
            self.actvcode[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "TASKPRED":
            obj = TaskPred(params)
            self.taskpred[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "TASKRSRC":
            obj = TaskRsrc(params)
            self.taskrsrc[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "TASKACTV":
            obj = TaskActv(params)
            self.taskactv[obj.get_id()] = obj
            return obj
        elif object_type.strip() == "UDFVALUE":
            obj = UDFValue(params)
            self.udfvalue[obj.get_id()] = obj
            return obj

    def summary(self):
        print('Number of activities: ', len(self.task))
        print('Number of relationships: ', len(self.taskpred))

    def get_task_by_id(self, task_id):
        print("task ID search", task_id)
        return Task.find_by_activity_id(task_id, self.task)

    def __init__(self, filename):
        #file = open('SP10 - COST LOADED.xer', 'r')
        file = open(filename, 'r')
        content = file.readlines()
        for line in content:
            line_lst = line.split('\t')
            if line_lst[0] == "%T":
                current_table = line_lst[1]
            elif line_lst[0] == "%R":
                self.create_object(current_table, line_lst[1:])


# r = Reader('model/SP10 - COST LOADED.xer')
# print(r)
# print(r.task)
#
# print(r.get_task_by_id('P1EWCC-FWP03-5710'))
# print(Task.find_by_activity_id('P1EWCC-FWP03-5710', r.task))