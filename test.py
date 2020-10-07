import time

from xerparser import *
from xerparser.reader import Reader
from collections import defaultdict

start_time = time.time()
r = Reader('xerparser/model/trial6.xer')
elapsed_time1 = time.time() - start_time
print(elapsed_time1)
# trial4 trial12

# for p in r.projects:
#     for wbs in p.wbss:
#         for act in wbs.activities:
#             for rel in act.successors:
#                 print("Project", p, "\t\t WBS: ", wbs, "\t\t\tActivity: ", act.task_code, "\t\tRel:", rel)
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

start_time = time.time()
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

print("time to read the file only {}".format(elapsed_time1))
# print("Time to create tree file", elapsed_time, "activities: ", len(r.tasks), "rels ", len(r.relations))