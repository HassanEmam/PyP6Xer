
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
    def __init__(self, programme, duration_limit=1, lag_limit=0):
        self.count = 0
        self.programme = programme
        self.dur_limit = duration_limit
        self.lag_limit = lag_limit
        self.results = {}
        self.results['analysis'] = {}


    def analysis(self):
        self.activity_count = len(self.programme.activities)
        self.relation_count = len(self.programme.relations)
        self.results['analysis']['summary'] = {'activity_cnt': self.activity_count, 'relationship_cnt': self.relation_count}
        # 1 successors
        self.no_successors = self.chk_successors()
        self.no_successors_cnt = len(self.no_successors)
        self.results['analysis']['successors'] = {'cnt': self.no_successors_cnt,
                                                  'activities': self.no_successors,
                                                  'pct': self.no_successors_cnt / float(self.activity_count)}
        #2 predecessors
        self.no_predecessors = self.chk_predessors()
        self.no_predecessors_cnt = len(self.no_predecessors)
        self.results['analysis']['predecessors'] = {'cnt': self.no_predecessors_cnt,
                                                    'activities': self.no_predecessors,
                                                    'pct': self.no_predecessors_cnt / float(self.activity_count)}
        #3 durations
        self.duration = list(filter(lambda x: x.duration > self.dur_limit,  self.programme.activities.activities))
        self.results['analysis']['duration'] = {'cnt': len(self.duration),
                                                'activities': self.duration,
                                                'pct': len(self.duration) / float(self.activity_count)}
        #4 leads
        self.leads = self.programme.relations.leads
        self.results['analysis']['leads'] = {'cnt': len(self.leads),
                                             'relations': self.leads,
                                             'pct': len(self.leads) / float(self.relation_count)}
        #5 lags
        self.lags = list(filter(lambda x: x.lag_hr_cnt > self.lag_limit if x.lag_hr_cnt else None, self.programme.relations))
        self.results['analysis']['lags'] = {'cnt': len(self.lags),
                                            'relations': self.lags,
                                            'pct': len(self.lags) / float(self.relation_count)}
        #6 relationships
        self.fsRel = self.programme.relations.finish_to_start
        self.results['analysis']['relations'] = {'fs_cnt': len(self.fsRel), 'relationship': self.fsRel}
        #7 constraints
        lst = ['CS_MANDFIN', 'CS_MANDFIN']
        self.constraints = list(filter(lambda x: x.get('ConstraintType') in lst, self.programme.activities.constraints))
        self.results['analysis']['constraints'] = {'cstr_cnt': len(self.constraints), 'cstrs': self.constraints}
        return self.results

    def chk_successors(self):
        return self.programme.activities.has_no_successor

    def chk_predessors(self):
        return self.programme.activities.has_no_predecessor