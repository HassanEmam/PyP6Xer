from xerparser import *
from xerparser.reader import Reader
r = Reader('xerparser/model/AA.xer')

activities = r.tasks.has_no_successor
for act in activities:
    print(act.task_code, act.task_name, act)

act = r.tasks.activities_by_activity_code_id(3207)
# print(r.tasks)
# rate = ResourceRate.find_by_resource_id(8898)
# print(rate)
# code_types = ActType.obj_list
code_type = ActType.find_by_id(206).get_activity_codes()
print(code_type)
print(r.tasks.count)
# if rate:
#     print("Rate", rate, rate.role_id, rate.cost_per_qty)
# for activity in activities:
#     print(activity.task_code + '\t\t' + activity.task_name + '\t\t\t\t' + str(activity.get_duration()) + '\t' + str(activity.early_start_date) + '\t\t' + str(activity.early_end_date))
