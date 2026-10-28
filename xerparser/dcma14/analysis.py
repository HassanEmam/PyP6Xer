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


class DCMA14():
    """DCMA 14-point analysis for project schedule quality assessment.

    This class performs a comprehensive analysis of a project schedule
    based on the Defense Contract Management Agency (DCMA) 14-point
    assessment criteria.

    Parameters:
        programme: The project programme/schedule to analyze
        duration_limit (int): Threshold for activity duration analysis (default: 1)
        lag_limit (int): Threshold for relationship lag analysis (default: 0)
        tf_limit (int): Threshold for total float analysis (default: 0)

    Returns:
        Analysis results in the following structure::

            {
                "analysis": {
                    "summary": {"activity_cnt": int, "relationship_cnt": int},
                    "predecessors": {"cnt": int, "activities": list, "pct": float},
                    "successors": {"cnt": int, "activities": list, "pct": float},
                    "lags": {"cnt": int, "relations": list, "pct": float},
                    "leads": {"cnt": int, "relations": list, "pct": float},
                    "relations": {"fs_cnt": int, "relationship": list},
                    "constraints": {"cstr_cnt": int, "cstrs": list},
                    "totalfloat": {"cnt": int, "activities": list, "pct": float},
                    "negativefloat": {"cnt": int, "activities": list, "pct": float},
                    "duration": {"cnt": int, "activities": list, "pct": float},
                    "invaliddates": {"cnt": int, "pct": float},
                    "resources": {"cnt": int, "activities": list, "pct": float},
                    "slippage": {"cnt": int, "activities": list, "pct": float},
                    "critical": {"cnt": int, "activities": list, "pct": float},
                    "critical_test": {"longest_chain_cnt": int, "passed": bool},
                    "cpli": {"critical_path_length": float, "total_float": float, "cpli": float},
                    "bei": {"earned": int, "required": int, "bei": float}
                }
            }
    """
    # XER cstr_type codes counted as "hard constraints" by DCMA check #5:
    # Mandatory Start (CS_MSO), Mandatory Finish (CS_MEO),
    # Start On (CS_SON) and Finish On (CS_FON).
    HARD_CONSTRAINTS = ('CS_MSO', 'CS_MEO', 'CS_SON', 'CS_FON')

    def __init__(self, programme, duration_limit=1, lag_limit=0, tf_limit=0):
        self.count = 0
        self.programme = programme
        self.dur_limit = duration_limit
        self.lag_limit = lag_limit
        self.tf_limit = tf_limit
        self.results = {}
        self.results['analysis'] = {}

    @staticmethod
    def _day_hours(activity):
        """Working hours per day for the activity's calendar (fallback 8.0)."""
        cal = getattr(activity, 'calendar', None)
        if cal is not None and getattr(cal, 'day_hr_cnt', None):
            return float(cal.day_hr_cnt)
        return 8.0

    def analysis(self):
        """Perform the complete DCMA 14-point analysis.

        Returns:
            dict: Analysis results containing all 14 assessment points
        """
        self.activity_count = len(self.programme.activities)
        self.relation_count = len(self.programme.relations)
        self.results['analysis']['summary'] = {'activity_cnt': self.activity_count, 'relationship_cnt': self.relation_count}
        # 1.1 successors
        self.no_successors = self.chk_successors()
        self.no_successors_cnt = len(self.no_successors)
        self.results['analysis']['successors'] = {'cnt': self.no_successors_cnt,
                                                  'activities': [self.get_activity(x.task_id) for x in self.no_successors],
                                                  'pct': self._safe_ratio(self.no_successors_cnt, self.activity_count)}
        #1.2 predecessors
        self.no_predecessors = self.chk_predessors()
        self.no_predecessors_cnt = len(self.no_predecessors)
        self.results['analysis']['predecessors'] = {'cnt': self.no_predecessors_cnt,
                                                    'activities': [self.get_activity(x.task_id) for x in self.no_predecessors],
                                                    'pct': self._safe_ratio(self.no_predecessors_cnt, self.activity_count)}
        #2 lags
        self.lags = list(filter(lambda x: x.lag_hr_cnt > self.lag_limit if x.lag_hr_cnt else None, self.programme.relations))
        self.results['analysis']['lags'] = {'cnt': len(self.lags),
                                            'relations': [ {
                                                            "successor":self.get_activity(x.task_id),
                                                            "predecessor":self.get_activity(x.pred_task_id),
                                                            "type": x.pred_type,
                                                            "lag": self._hours_to_days(x.lag_hr_cnt)
                                                            } for x in self.lags],
                                            'pct': self._safe_ratio(len(self.lags), self.relation_count)}
        #3 leads
        self.leads = self.programme.relations.leads
        self.results['analysis']['leads'] = {'cnt': len(self.leads),
                                             'relations': [{
                                                            "successor":self.get_activity(x.task_id),
                                                            "predecessor":self.get_activity(x.pred_task_id),
                                                            "type": x.pred_type,
                                                            "lag": self._hours_to_days(x.lag_hr_cnt)
                                                            } for x in self.leads],
                                             'pct': self._safe_ratio(len(self.leads), self.relation_count)}
        #4 relationships
        self.fsRel = self.programme.relations.finish_to_start
        self.results['analysis']['relations'] = {'fs_cnt': len(self.fsRel), 'relationship': [
                                                {
                                                    "successor":self.get_activity(x.task_id),
                                                    "predecessor":self.get_activity(x.pred_task_id),
                                                    "type": x.pred_type,
                                                    "lag": self._hours_to_days(x.lag_hr_cnt)
                                                    } for x in self.fsRel]}
        #5 constraints (hard constraints per DCMA: Mandatory Start/Finish, Start On/Finish On)
        self.constraints = list(filter(lambda x: x.cstr_type and x.cstr_type in self.HARD_CONSTRAINTS,
                                        self.programme.activities))
        self.results['analysis']['constraints'] = {'cstr_cnt': len(self.constraints),
                                                    'cstrs': [self.get_activity(x.task_id) for x in self.constraints]}
        #6 large total float
        self.totalfloat = list(filter(lambda x: x.total_float_hr_cnt is not None and x.total_float_hr_cnt / self._day_hours(x) > self.tf_limit,  self.programme.activities.activities))
        self.results['analysis']['totalfloat'] = {'cnt': len(self.totalfloat),
                                                'activities': [self.get_activity(x.task_id) for x in self.totalfloat],
                                                'pct': self._safe_ratio(len(self.totalfloat), self.activity_count)}
        #7 negative total float
        self.negativefloat = list(filter(lambda x: x.total_float_hr_cnt is not None and x.total_float_hr_cnt / self._day_hours(x) < 0,  self.programme.activities.activities))
        self.results['analysis']['negativefloat'] = {'cnt': len(self.negativefloat),
                                                'activities': [self.get_activity(x.task_id) for x in self.negativefloat],
                                                'pct': self._safe_ratio(len(self.negativefloat), self.activity_count)}
        #8 durations
        self.duration = list(filter(lambda x: x.duration > self.dur_limit,  self.programme.activities.activities))
        self.results['analysis']['duration'] = {'cnt': len(self.duration),
                                                'activities': [self.get_activity(x.task_id) for x in self.duration],
                                                'pct': self._safe_ratio(len(self.duration), self.activity_count)}
        #9 Check for Invalid Dates
        # no actual dates beyond data date
        data_date = self._data_dates()
        self.invalidactualstart = list(filter(lambda x: x.proj_id is not None and x.act_start_date is not None and x.act_start_date > data_date[str(x.proj_id)], self.programme.activities.activities))
        self.invalidactualfinish = list(filter(lambda x: x.proj_id is not None and x.act_end_date is not None and x.act_end_date > data_date[str(x.proj_id)], self.programme.activities.activities))
        self.invalidearlystart = list(filter(lambda x: x.proj_id is not None and x.early_start_date is not None and x.early_start_date < data_date[str(x.proj_id)], self.programme.activities.activities))
        self.invalidearlyfinish = list(filter(lambda x: x.proj_id is not None and x.early_end_date is not None and x.early_end_date < data_date[str(x.proj_id)], self.programme.activities.activities))
        # DCMA denominator = number of activities with at least one invalid date
        invalid_activities = set()
        for lst in (self.invalidactualstart, self.invalidactualfinish,
                    self.invalidearlystart, self.invalidearlyfinish):
            for x in lst:
                invalid_activities.add(x.task_id)
        cnt = len(invalid_activities)
        pct = self._safe_ratio(cnt, self.activity_count)
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
            'pct': self._safe_ratio(len(no_resources), self.activity_count)
        }

        #11 slippage from target
        # end dates are later than target end dates
        self.actualendslippage = list(filter(lambda x: x.act_end_date is not None and x.target_end_date is not None and x.act_end_date > x.target_end_date, self.programme.activities.activities))
        self.earlyendslippage = list(filter(lambda x: x.early_end_date is not None and x.target_end_date is not None and x.early_end_date > x.target_end_date, self.programme.activities.activities))
        # DCMA counts activities, not relations: an activity slipping on both its
        # actual and early end is counted once.
        slipped = {x.task_id: x for x in self.actualendslippage + self.earlyendslippage}
        slipped = list(slipped.values())
        self.results['analysis']['slippage'] = {
            'activities': [{
                "id":x.task_code,
                "name": x.task_name,
                "early_finish": str(x.early_end_date),
                "planned_finish": str(x.target_end_date)
            } for x in slipped],
            'cnt': len(slipped),
            'pct': self._safe_ratio(len(slipped), self.activity_count)
        }

        #12 Critical Path Test
        critical = self._critical_activities()
        chain = self._longest_critical_chain(critical)
        self.results['analysis']['critical_test'] = {
            'longest_chain_cnt': len(chain),
            'passed': len(chain) >= 2
        }

        #13 Critical Path Length Index
        # CPLI = critical path length / (critical path length + total float),
        # where total float is the largest float of any non-critical, incomplete activity.
        cp_length = sum(a.target_drtn_hr_cnt or 0 for a in chain)
        noncritical = [a for a in self.programme.activities.activities
                       if a not in chain and a.status_code != 'TK_Complete'
                       and a.total_float_hr_cnt is not None]
        total_float = max((a.total_float_hr_cnt for a in noncritical), default=0.0)
        if cp_length + total_float > 0:
            cpli = cp_length / (cp_length + total_float)
        else:
            cpli = None
        self.results['analysis']['cpli'] = {
            'critical_path_length': cp_length,
            'total_float': total_float,
            'cpli': cpli
        }

        self.results['analysis']['critical'] = {
            'activities': [self.get_activity(x.task_id) for x in critical],
            'cnt': len(critical),
            'pct': self._safe_ratio(len(critical), self.activity_count)
        }

        #14 Baseline Execution Index (BEI)
        # earned = activities with an actual start or finish;
        # required = activities whose baseline (target) start date is on or before the data date.
        latest_dd = max(data_date.values()) if data_date else None
        if latest_dd is not None:
            earned = len([a for a in self.programme.activities.activities
                          if a.act_start_date is not None or a.act_end_date is not None])
            required = len([a for a in self.programme.activities.activities
                            if a.target_start_date is not None and a.target_start_date <= latest_dd])
            bei = self._safe_ratio(earned, required) if required > 0 else None
            self.results['analysis']['bei'] = {'earned': earned, 'required': required, 'bei': bei}
        else:
            self.results['analysis']['bei'] = {'earned': 0, 'required': 0, 'bei': None}

        return self.results

    def _critical_activities(self):
        """Activities that are not complete and have total float <= 0."""
        return [a for a in self.programme.activities.activities
                if a.status_code != 'TK_Complete'
                and a.total_float_hr_cnt is not None
                and a.total_float_hr_cnt <= 0]

    def _longest_critical_chain(self, critical):
        """Longest continuous chain of FS relationships within the critical set.

        Implements a practical version of DCMA check #12: the critical
        activities must form at least one continuous logic path.
        """
        if len(critical) < 2:
            return list(critical)
        crit_ids = {a.task_id for a in critical}
        crit_by_id = {a.task_id: a for a in critical}
        # adjacency: successor -> list of critical predecessors
        preds = {}
        referenced = set()
        for rel in self.programme.relations:
            if rel.task_id in crit_ids and rel.pred_task_id in crit_ids and rel.pred_type == 'PR_FS':
                preds.setdefault(rel.task_id, []).append(rel.pred_task_id)
                referenced.add(rel.pred_task_id)
        # Walk from successors towards predecessors: a maximal chain starts at a
        # critical activity that is nobody's critical predecessor (no critical successors).
        starts = [tid for tid in crit_ids if tid not in referenced]
        if not starts:
            starts = list(crit_ids)  # cycle: fall back to every node
        best = []
        for start in starts:
            path = self._dfs_longest(start, preds, crit_by_id)
            if len(path) > len(best):
                best = path
        return best

    def _dfs_longest(self, node, preds, crit_by_id):
        """DFS from a start node following predecessor links; returns longest path."""
        stack_paths = [[node]]
        best = [node]
        while stack_paths:
            path = stack_paths.pop()
            last = path[-1]
            extended = False
            for p in preds.get(last, []):
                if p in path:  # guard against cycles
                    continue
                new_path = path + [p]
                stack_paths.append(new_path)
                extended = True
                if len(new_path) > len(best):
                    best = new_path
            if not extended and len(path) > len(best):
                best = path
        return [crit_by_id[n] for n in best]

    def _data_dates(self):
        """Data date per project id (last_recalc_date), current date as fallback."""
        data_date = {}
        for x in self.programme.projects:
            if x.last_recalc_date and x.last_recalc_date.strip():
                try:
                    data_date[str(x.proj_id)] = datetime.strptime(x.last_recalc_date, "%Y-%m-%d %H:%M")
                except ValueError:
                    data_date[str(x.proj_id)] = datetime.now()
            else:
                data_date[str(x.proj_id)] = datetime.now()
        return data_date

    def _hours_to_days(self, lag_hr_cnt):
        return int(lag_hr_cnt / 8.0) if lag_hr_cnt else 0

    @staticmethod
    def _safe_ratio(numerator, denominator):
        return numerator / float(denominator) if denominator else 0.0

    def chk_successors(self):
        """Check for activities with no successors.

        Returns:
            list: Activities that have no successor relationships
        """
        return self.programme.activities.has_no_successor

    def chk_predessors(self):
        """Check for activities with no predecessors.

        Returns:
            list: Activities that have no predecessor relationships
        """
        return self.programme.activities.has_no_predecessor

    def get_activity(self, id):
        """Get activity information by ID.

        Args:
            id: Activity ID to retrieve

        Returns:
            dict or None: Activity information including id, name, duration, and total float
        """
        activity = self.programme.activities.find_by_id(id)
        if type(activity) == list:
            return None
        return {
                "id": activity.task_code,
                "name": activity.task_name,
                "duration": activity.duration,
                "tf": activity.total_float_hr_cnt / self._day_hours(activity) if activity.total_float_hr_cnt else 0
                }
