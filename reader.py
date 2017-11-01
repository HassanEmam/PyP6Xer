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
    currencies = []
    obs = []
    rcattype = []
    udftype = []
    rcatval = []
    project = []
    calendar = []
    schedoption = []
    wbs = []
    resource = []
    acttype = []
    rsrcrate = []
    rsrcrcat = []
    task = []
    actvcode = []
    taskpred = []
    taskrsrc = []
    taskactv = []
    udfvalue = []

    def create_object(self, object_type, params):

        """

        Args:
            object_type:
            params:

        Returns:

        """
        if object_type.strip() == "CURRTYPE":
            obj = Currency(params)
            self.currencies.append(obj)
            return obj
        elif object_type.strip() == "OBS":
            obj = OBS(params)
            self.obs.append(obj)
            return obj
        elif object_type.strip() == "RCATTYPE":
            obj = RCatType(params)
            self.rcattype.append(obj)
            return obj
        elif object_type.strip() == "UDFTYPE":
            obj = UDFType(params)
            self.udftype.append(obj)
            return obj
        elif object_type.strip() == "RCATVAL":
            obj = RCatVal(params)
            self.rcatval.append(obj)
            return obj
        elif object_type.strip() == "PROJECT":
            obj = Project(params)
            self.project.append(obj)
            return obj
        elif object_type.strip() == "CALENDAR":
            obj = Calendar(params)
            print(params)
            self.calendar.append(obj)
            return obj
        elif object_type.strip() == "SCHEDOPTIONS":
            obj = SchedOption(params)
            self.schedoption.append(obj)
            return obj
        elif object_type.strip() == "PROJWBS":
            obj = WBS(params)
            self.wbs.append(obj)
            return obj
        elif object_type.strip() == "RSRC":
            obj = Resource(params)
            self.resource.append(obj)
            return obj
        elif object_type.strip() == "ACTVTYPE":
            obj = ActType(params)
            self.acttype.append(obj)
            return obj
        elif object_type.strip() == "RSRCRATE":
            obj = ResourceRate(params)
            self.rsrcrate.append(obj)
            return obj
        elif object_type.strip() == "RSRCRCAT":
            obj = ResourceCat(params)
            self.rsrcrcat.append(obj)
            return obj
        elif object_type.strip() == "TASK":
            obj = Task(params)
            #self.task.append(obj)
            return obj
        elif object_type.strip() == "ACTVCODE":
            obj = ActivityCode(params)
            self.actvcode.append(obj)
            return obj
        elif object_type.strip() == "TASKPRED":
            obj = TaskPred(params)
            self.taskpred.append(obj)
            return obj
        elif object_type.strip() == "TASKRSRC":
            obj = TaskRsrc(params)
            self.taskrsrc.append(obj)
            return obj
        elif object_type.strip() == "TASKACTV":
            obj = TaskActv(params)
            self.taskactv.append(obj)
            return obj
        elif object_type.strip() == "UDFVALUE":
            obj = UDFValue(params)
            self.udfvalue.append(obj)
            return obj

    def summary(self):
        print('Number of activities: ', len(self.task))
        print('Number of relationships: ', len(self.taskpred))

    def __init__(self, filename):
        file = open(filename, 'r')
        content = file.readlines()
        for line in content:
            line_lst = line.split('\t')
            if line_lst[0] == "%T":
                current_table = line_lst[1]
            elif line_lst[0] == "%R":
                self.create_object(current_table, line_lst[1:])


r = Reader('model/SP10 - COST LOADED.xer')
# for acode in r.get_activity_codes():
#     print(acode)
t = Task.find_by_code('P1EWCC-PWP02-4100')
print('type', t.cstr_type, t.cstr_date, t.driving_path_flag, t.get_duration())
t = t.obj_list
# print(r.task)
actvCode = Calendar.find_by_id('639')

tasks = Task.float_less_than(0)

for task in tasks:
    print(task.task_code, task.total_float_hr_cnt/float(task.calendar.day_hr_cnt))
    print(task.calendar.clndr_name, task.calendar.working_days)
