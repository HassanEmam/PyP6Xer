import time
import csv
import re
from xerparser import *
from xerparser.reader import Reader
from xerparser.dcma14 import DCMA14
from collections import defaultdict

start_time = time.time()
r = Reader('sample.xer')
# print("Reader OUTCOME", r)
elapsed_time1 = time.time() - start_time
# # print(elapsed_time1)
# for prj in r.projects:
#     # print(len(prj.wbss), prj.wbss)
#     for wbs in prj.wbss:
#         for act in wbs.activities:
#             # print(wbs, act.task_name)
#             for res in act.resources:
#                 print(res)
#             for actv in act.activitycodes:
#                 print(actv)

# r = Reader('CONSRTRUCTION.xer')
# # print("Reader OUTCOME", r)
# elapsed_time1 = time.time() - start_time
# # print(elapsed_time1)
# for prj in r.projects:
#     # print(len(prj.wbss), prj.wbss)
#     for wbs in prj.wbss:
#         for act in wbs.activities:
#             # print(wbs, act.task_name)
#             for res in act.resources:
#                 print(res)
#             for actv in act.activitycodes:
#                 print(actv)
# # for account in r.accounts:
# #     print(account)

# for act in r.activities:
#     critical = []
#     # print(act.total_float_hr_cnt)
#     if act.total_float_hr_cnt is not None:
#         if act.total_float_hr_cnt <= 0:
#             print("TF FOUND", act.task_code, act.total_float_hr_cnt)
            
#             critical.append(act)
#     else:
#         print("TF Not found")

# print(r)
# r.write("hassan.xer")

#
# for actrsrc in r._activityresources:
#     print(actrsrc, actrsrc.taskrsrc_id)
#
# print(r.activityresources.find_by_id(5157763))

# for actcode in r.actvcodes:
#     print(actcode, actcode.actv_code_type_id)
# print("Code", r.actvcodes.find_by_id(798526))
# print("Code", r.actvcodes.find_by_type_id(87933))

# for type in r.acttypes:
#     print(type, type.actv_code_type_id)
# print(r.acttypes.find_by_id(87934))

# for cal in r.calendars:
#     print(cal.clndr_id, cal)
# print(r.calendars.find_by_id(94905))

# for cur in r.currencies:
#     print(cur.curr_id, cur)
# print(r.currencies.find_by_id(51))

# for pred in r.relations:
#     print(pred, pred.task_pred_id, pred.pred_task_id)
# print(r.relations.get_predecessors(9478273))



# for cal in r.calendars:
#     print(cal.clndr_name)
#     print(cal.working_days)
#     print(cal.working_hours)
#     print(cal.exceptions)
#     print(dir(cal))
# trial4 trial12

# for taskact in r.actvcodes:
#     print(taskact)
# 
# for resource in r.resources:
#     print(resource)
# 
# for rsrc in r.activityresources:
#     task = r.activities.find_by_id(rsrc.rsrc_id)
#     resource = r.resources.get_resource_by_id(rsrc.task_id)
#     print(rsrc, task, resource)

# get wbs elements and activities for all projects in a single xer file
# =====================================================================
# for p in r.projects:
#     for wbs in p.wbss:
#         for act in wbs.activities:
#             print(act, act.activitycodes)
#
# print("Project has {} activities".format(r.tasks.count))
# resor = []
# for res in r.resources:
#     resor.append((res.rsrc_id, res.parent_rsrc_id))
# print(resor)
# # a = [(24675, 3656), (24677, 24675), (24678, 24675), (24679, 24675), (25445, 24675), (25515, 24675), (25516, 24675), (25555, 24675), (25556, 24675), (25557, 24675), (26196, 24675), (26653, 24675), (27114, 27113), (27383, 24675), (27403, 24675), (30875, 24675), (31132, 24675), (31284, 24675), (31986, 3656), (34063, 24675), (34116, 24675), (34122, 24675), (1577, None)]
# a = resor[:]
# # pass 1: create nodes dictionary
# nodes = {}
# for i in a:
#     id, parent_id = i
#     nodes[id] = { 'id': id }
# # a = a[1:]
# # pass 2: create trees and parent-child relations
# forest = []
# for i in a:
#     id, parent_id = i
#     node = nodes[id]
#
#     # either make the node a new tree or link it to its parent
#     if parent_id == None:
#         # start a new tree in the forest
#         forest.append(node)
#     else:
#         # add new_node as child to parent
#         parent = nodes[parent_id]
#         if not 'children' in parent:
#             # ensure parent has a 'children' field
#             parent['children'] = []
#         children = parent['children']
#         children.append(node)
# print(forest)

# tree = r.resources.build_tree()
# print(tree)

# start_time = time.time()
#
# data = {}
# for p in r._projects:
#     for wbs in p.wbss:
#         if p.proj_id in data:
#             data[p.proj_id][wbs] = wbs.activities
#         else:
#             data = defaultdict(dict)
#             data[p.proj_id][wbs] = wbs.activities
# for act in wbs.activities:
#     data[p.proj_id][wbs].append(act)
# elapsed_time = time.time() - start_time
#
# import pprint
# pp = pprint.PrettyPrinter(depth=4)
# pp.pprint(tree)

# pp.pprint(data)
# for t in r.tasks:
#     print(t.task_id, t, t.resources)
# print("time to read the file only {}".format(elapsed_time1))
# print("Time to create tree file", elapsed_time, "activities: ", len(r.tasks), "rels ", len(r.relations))

# for cal in r.calendars:
#     print(cal)
#
# for a in r.activities:
#     print(a.resources)

# print(Reader.activities.__doc__)
# print(Reader.__doc__)
# print(help(Reader))
# print(r.projects)

# health = DCMA14(r)
# print(health.analysis())
#print(health.no_successors_cnt, health.no_successors)
#print(health.no_predecessors_cnt, health.no_predecessors)

# import pprint
# pp = pprint.PrettyPrinter(depth=4)
# print(r.relations.relations)
#print(health.results['analysis']['lags'])
#print(health.results['analysis']['leads'])

# pp.pprint(health.results['analysis']['constraints'])

for project in r.projects:
    print("PROJECT: " + project.proj_short_name + "*****")
    for activity in project.activities:
        print("################### Activity ID | ", activity.task_code, " | Activity Name | ", activity.task_name, " | Pred |", activity.predecessors)
