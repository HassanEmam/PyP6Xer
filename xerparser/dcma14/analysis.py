# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.
from datetime import datetime
from logging import critical


class DCMA14():
    """

    {Analysis :
        {
        Predecessors: {
            cnt : 45
            tasks: []
            }
        },
        successors: {
            cnt: 30,
            tasks: []
        }
    """
    def __init__(self, programme, duration_limit=1, lag_limit=0, tf_limit=0):
        self.count = 0
        self.programme = programme
        self.dur_limit = duration_limit
        self.lag_limit = lag_limit
        self.tf_limit = tf_limit
        self.results = {}
        self.results['analysis'] = {}


    def analysis(self):
        self.activity_count = len(self.programme.activities)
        self.relation_count = len(self.programme.relations)
        self.results['analysis']['summary'] = {'activity_cnt': self.activity_count, 'relationship_cnt': self.relation_count}
        # 1.1 successors
        self.no_successors = self.chk_successors()
        self.no_successors_cnt = len(self.no_successors)
        self.results['analysis']['successors'] = {'cnt': self.no_successors_cnt,
                                                  'activities': [self.get_activity(x.task_id) for x in self.no_successors],
                                                  'pct': self.no_successors_cnt / float(self.activity_count)}
        #1.2 predecessors
        self.no_predecessors = self.chk_predessors()
        self.no_predecessors_cnt = len(self.no_predecessors)
        self.results['analysis']['predecessors'] = {'cnt': self.no_predecessors_cnt,
                                                    'activities': [self.get_activity(x.task_id) for x in self.no_predecessors],
                                                    'pct': self.no_predecessors_cnt / float(self.activity_count)}
        #2 lags
        self.lags = list(filter(lambda x: x.lag_hr_cnt > self.lag_limit if x.lag_hr_cnt else None, self.programme.relations))
        self.results['analysis']['lags'] = {'cnt': len(self.lags),
                                            'relations': [ { 
                                                            "successor":self.get_activity(x.task_id),
                                                            "predecessor":self.get_activity(x.pred_task_id),
                                                            "type": x.pred_type,
                                                            "lag": int(x.lag_hr_cnt / 8.0)
                                                            } for x in self.lags],
                                            'pct': len(self.lags) / float(self.relation_count)}
        #3 leads
        self.leads = self.programme.relations.leads
        self.results['analysis']['leads'] = {'cnt': len(self.leads),
                                             'relations': [{ 
                                                            "successor":self.get_activity(x.task_id),
                                                            "predecessor":self.get_activity(x.pred_task_id),
                                                            "type": x.pred_type,
                                                            "lag": int(x.lag_hr_cnt / 8.0)
                                                            } for x in self.leads],
                                             'pct': len(self.leads) / float(self.relation_count)}
        #4 relationships
        self.fsRel = self.programme.relations.finish_to_start
        self.results['analysis']['relations'] = {'fs_cnt': len(self.fsRel), 'relationship': [
                                                { 
                                                    "successor":self.get_activity(x.task_id),
                                                    "predecessor":self.get_activity(x.pred_task_id),
                                                    "type": x.pred_type,
                                                    "lag": int(x.lag_hr_cnt / 8.0)
                                                    } for x in self.fsRel]}
        #5 constraints
        lst = ['CS_MANDFIN', 'CS_MANDFIN']
        self.constraints = list(filter(lambda x: x.get('ConstraintType') in lst,
                                        self.programme.activities))
        self.results['analysis']['constraints'] = {'cstr_cnt': len(self.constraints), 
                                                    'cstrs': [self.get_activity(x.task_id) for x in self.constraints]}
        #6 large total float
        self.totalfloat = list(filter(lambda x: x.total_float_hr_cnt /8.0 > self.tf_limit if x.total_float_hr_cnt else 0,  self.programme.activities.activities))
        self.results['analysis']['totalfloat'] = {'cnt': len(self.totalfloat),
                                                'activities': [self.get_activity(x.task_id) for x in self.totalfloat],
                                                'pct': len(self.totalfloat) / float(self.activity_count)}
        #7 negative total float
        self.negativefloat = list(filter(lambda x: x.total_float_hr_cnt /8.0 < 0 if x.total_float_hr_cnt else 0,  self.programme.activities.activities))
        self.results['analysis']['negativefloat'] = {'cnt': len(self.negativefloat),
                                                'activities': [self.get_activity(x.task_id) for x in self.negativefloat],
                                                'pct': len(self.negativefloat) / float(self.activity_count)}
        #8 durations
        self.duration = list(filter(lambda x: x.duration > self.dur_limit,  self.programme.activities.activities))
        self.results['analysis']['duration'] = {'cnt': len(self.duration),
                                                'activities': [self.get_activity(x.task_id) for x in self.duration],
                                                'pct': len(self.duration) / float(self.activity_count)}
        #9 Check for Invalid Dates
        # no actual dates beyong data date
        data_date = {}
        for x in self.programme.projects:
            data_date[str(x.proj_id)] = datetime.strptime(x.last_recalc_date, "%Y-%m-%d %H:%M")
        print(data_date)
        self.invalidactualstart = list(filter(lambda x: None if x.act_start_date is None else x.act_start_date > data_date[str(x.proj_id)], self.programme.activities.activities))
        self.invalidactualfinish = list(filter(lambda x: None if x.act_end_date is None else x.act_end_date > data_date[str(x.proj_id)], self.programme.activities.activities))
        self.invalidearlystart = list(filter(lambda x: None if x.early_start_date is None else x.early_start_date < data_date[str(x.proj_id)], self.programme.activities.activities))
        self.invalidearlyfinish = list(filter(lambda x: None if x.early_end_date is None else x.early_end_date < data_date[str(x.proj_id)], self.programme.activities.activities))
        cnt = len(self.invalidactualfinish) + len(self.invalidactualstart) + len(self.invalidearlystart) + len(self.invalidearlyfinish)
        pct = cnt / float(self.activity_count)
        self.invaliddates = {
            "actual_start": [self.get_activity(x.task_id) for x in self.invalidactualstart],
            "actual_finish": [self.get_activity(x.task_id) for x in self.invalidactualfinish],
            "early_start": [self.get_activity(x.task_id) for x in self.invalidearlystart],
            "early_finish": [self.get_activity(x.task_id) for x in self.invalidearlyfinish],
            "cnt": cnt,
            'pct': pct
            }
        self.results['analysis']['invaliddates'] = self.invaliddates

        #10 Check resource assignments
        no_resources = []
        tasks_id = [x.task_id for x in self.programme.activities.activities]
        for t_id in tasks_id:
            assignments = self.programme.activityresources.find_by_activity_id(t_id)
            if len(assignments) == 0:
                no_resources.append(t_id)
        self.results['analysis']['resources'] = {
            'activities': [self.get_activity(x) for x in no_resources],
            "cnt": len(no_resources),
            'pct': len(no_resources) / float(self.activity_count)
        }
        print(no_resources)

        #11 slippage from target
        # end dates are later than target end dates
        self.actualendslippage = list(filter(lambda x: None if x.act_end_date is None else x.act_end_date > x.target_end_date, self.programme.activities.activities))
        self.earlyendslippage = list(filter(lambda x: None if x.early_end_date is None else x.early_end_date > x.target_end_date, self.programme.activities.activities))
        slipped = self.actualendslippage + self.earlyendslippage
        print("SLIPPED", slipped)
        self.results['analysis']['slippage'] = {
            'activities': [{
                "id":x.task_code,
                "name": x.task_name,
                "early_finish": str(x.early_end_date),
                "planned_finish": str(x.target_end_date)
            } for x in slipped],
            'cnt': len(slipped),
            'pct': len(slipped) / float(self.activity_count)
        }

        #12 Critical Path Test
         
        
        #13 Critical Path Length Index
        # calculated as cirical path length + total float / critical path length
        # critical = list(filter(lambda x: x.total_float_hr_cnt <= 10.0 if x.total_float_hr_cnt else None, self.programme.activities.activities))
        critical = []
        for act in self.programme.activities.activities:
            if act.total_float_hr_cnt is not None:
                print("TF FOUND", act.task_code, act.total_float_hr_cnt)
                if act.total_float_hr_cnt <= 0:
                    
                    critical.append(act)
            else:
                print("TF Not found")


        print("critical", [(task.task_code, task.early_start_date, task.total_float_hr_cnt) for task in critical])

        self.results['analysis']['critical'] = {
            'activities': [self.get_activity(x.task_id) for x in critical],
            'cnt': len(critical),
            'pct': len(critical) / self.activity_count
        }

        

        #14 BLEI


        return self.results

    def chk_successors(self):
        return self.programme.activities.has_no_successor

    def chk_predessors(self):
        return self.programme.activities.has_no_predecessor

    def get_activity(self, id):
        activity = self.programme.activities.find_by_id(id)
        # print(activity)
        if type(activity) == list:
            return None
        return {
                "id": activity.task_code, 
                "name": activity.task_name,
                "duration": activity.duration,
                "tf":activity.total_float_hr_cnt / 8.0 if activity.total_float_hr_cnt else 0
                }
