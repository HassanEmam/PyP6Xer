from xerparser import *
from xerparser.reader import Reader
r = Reader('xerparser/model/trial2.xer')



for p in r.projects:
    for wbs in p.wbss:
        for act in wbs.activities:
            for rel in act.successors:
                print("Project", p, "\t\t WBS: ", wbs, "\t\t\tActivity: ", act.task_code, "\t\tRel:", rel)

print("Project has {} activities".format(r.tasks.count))