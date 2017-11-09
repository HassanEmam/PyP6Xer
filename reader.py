'''
This file starts the process of reading and parsing xer files

'''
from model.p6codes import *
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
from model.roles import Role
from model.account import Account
from model.rolerate import RoleRate

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
            obj = Task(params)
            #self.task.append(obj)
            return obj
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


r = Reader('model/trial2.xer')

activities = Task.no_successors()
rate = RoleRate.find_by_role_id(1570)
# code_types = ActType.obj_list
# code_type = ActType.find_by_id(206).get_activity_codes()
print(Role.obj_list, Account.obj_list)
print(rate, rate.role_id, rate.cost_per_qty)
# for activity in activities:
#     print(activity.task_code + '\t\t' + activity.task_name + '\t\t\t\t' + str(activity.get_duration()) + '\t' + str(activity.early_start_date) + '\t\t' + str(activity.early_end_date))
