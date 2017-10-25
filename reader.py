'''
This file starts the process of reading and parsing xer files

'''

from currency import Currency
from obs import OBS
from udftypes import UDFType
from rcatval import RCatVal
from rcattype import RCatType
from project import Project
from calendar import Calendar
from schedoption import SchedOption
from wbs import WBS
from rsrc import Resource
from acttype import ActType
from rsrcrate import ResourceRate
from rsrcrcat import ResourceCat
from task import Task
from activitycode import ActivityCode
from taskpred import TaskPred
from taskrsrc import TaskRsrc
from taskactv import TaskActv
from udfvalue import UDFValue

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

def create_object(object_type, params):
    if object_type.strip() == "CURRTYPE":
        obj = Currency(params)
        currencies[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "OBS":
        obj = OBS(params)
        obs[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "RCATTYPE":
        obj = RCatType(params)
        rcattype[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "UDFTYPE":
        obj = UDFType(params)
        udftype[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "RCATVAL":
        obj = RCatVal(params)
        rcatval[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "PROJECT":
        obj = Project(params)
        project[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "CALENDAR":
        obj = Calendar(params)
        calendar[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "SCHEDOPTIONS":
        obj = SchedOption(params)
        schedoption[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "PROJWBS":
        obj = WBS(params)
        wbs[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "RSRC":
        obj = Resource(params)
        resource[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "ACTVTYPE":
        obj = ActType(params)
        acttype[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "RSRCRATE":
        obj = ResourceRate(params)
        rsrcrate[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "RSRCRCAT":
        obj = ResourceCat(params)
        rsrcrcat[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "TASK":
        obj = Task(params)
        task[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "ACTVCODE":
        obj = ActivityCode(params)
        actvcode[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "TASKPRED":
        obj = TaskPred(params)
        taskpred[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "TASKRSRC":
        obj = TaskRsrc(params)
        taskrsrc[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "TASKACTV":
        obj = TaskActv(params)
        taskactv[obj.get_id()] = obj
        return obj
    elif object_type.strip() == "UDFVALUE":
        obj = UDFValue(params)
        udfvalue[obj.get_id()] = obj
        return obj

file = open('SP10 - COST LOADED.xer', 'r')
content = file.readlines()
for line in content:
    line_lst = line.split('\t')
    if line_lst[0] == "%T":
        current_table = line_lst[1]
    elif line_lst[0] == "%R":
        create_object(current_table, line_lst[1:])

a = Task.find_by_activity_id('P1EWCC-FWP03-5710', task)
print(len(taskpred))
