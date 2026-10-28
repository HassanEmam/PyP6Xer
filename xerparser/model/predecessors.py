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


from xerparser.model.classes.taskpred import TaskPred
# from xerparser.model.classes.task import Task
from typing import List


class Predecessors:
    """Collection of TASKPRED relationship records.

    Editing API: :meth:`add_relationship`, :meth:`remove_relationship`
    and :meth:`replace_relationship` modify the collection in place;
    a subsequent ``writeXER`` writes the edited relationships back.
    """

    #: Legal P6 relationship types.
    PRED_TYPES = ("PR_FS", "PR_SS", "PR_FF", "PR_SF")

    def __init__(self):
        self.index=0
        self.task_pred = []
        # Wired by the Reader so add_relationship can validate tasks and
        # derive proj ids; standalone collections may pass tasks= explicitly.
        self._tasks = None

    def find_by_id(self, code_id) -> TaskPred:
        # str-tolerant: ids are read from the XER as strings but callers
        # naturally pass ints (e.g. from Task.task_id).
        obj = list(filter(lambda x: str(x.task_pred_id) == str(code_id), self.task_pred))
        if len(obj) > 0:
            return obj[0]
        return None
    
    def get_tsv(self):
        tsv = []
        if len(self.task_pred) > 0:
            tsv.append(['%T', 'TASKPRED'])
            tsv.append(['%F', 'task_pred_id', 'task_id', 'pred_task_id', 'proj_id', 'pred_proj_id',
               'pred_type', 'lag_hr_cnt', 'comments', 'float_path', 'aref', 'arls'])
            for pred in self.task_pred:
                tsv.append(pred.get_tsv())
        return tsv
        
    def add(self, params):
        pred = TaskPred(params)
        self.task_pred.append(pred)

    # ------------------------------------------------------------------
    # Editing API (issue #7: resequence relationships programmatically)
    # ------------------------------------------------------------------

    def _resolve_tasks(self, tasks):
        tasks = tasks if tasks is not None else self._tasks
        if tasks is None:
            return None
        return tasks

    @staticmethod
    def _find_task(tasks, task_id):
        """find_by_id that tolerates both None and [] miss results."""
        task = tasks.find_by_id(task_id)
        if not task:
            return None
        return task

    def next_task_pred_id(self):
        """Next free numeric task_pred_id (max existing numeric id + 1)."""
        numeric = [int(x.task_pred_id) for x in self.task_pred
                   if x.task_pred_id is not None and str(x.task_pred_id).isdigit()]
        return max(numeric, default=0) + 1

    def _check_type(self, pred_type):
        if pred_type not in self.PRED_TYPES:
            raise ValueError(
                f"pred_type must be one of {', '.join(self.PRED_TYPES)}, got {pred_type!r}")

    @staticmethod
    def _check_lag(lag_hr_cnt):
        if lag_hr_cnt is None:
            return None
        try:
            return float(lag_hr_cnt)
        except (TypeError, ValueError):
            raise ValueError(f"lag_hr_cnt must be a number, got {lag_hr_cnt!r}")

    def _check_duplicate(self, task_id, pred_task_id, pred_type):
        for rel in self.task_pred:
            if (rel.task_id == int(task_id) and rel.pred_task_id == int(pred_task_id)
                    and rel.pred_type == pred_type):
                raise ValueError(
                    f"Relationship {pred_task_id} -> {task_id} ({pred_type}) already exists")

    def add_relationship(self, task_id, pred_task_id, pred_type="PR_FS",
                         lag_hr_cnt=None, comments=None, proj_id=None,
                         pred_proj_id=None, tasks=None):
        """Add a relationship and return the new TaskPred.

        Args:
            task_id: id of the successor activity.
            pred_task_id: id of the predecessor activity.
            pred_type: one of PR_FS, PR_SS, PR_FF, PR_SF (default PR_FS).
            lag_hr_cnt: lag in hours; negative for leads. Optional.
            comments: optional comment text.
            proj_id: project of the successor; derived from the task when
                a Tasks collection is available (the Reader wires one).
            pred_proj_id: project of the predecessor. Defaults to
                ``proj_id``; set it explicitly for cross-project links.
            tasks: Tasks collection used for validation/project lookup.
                Optional when the Reader wired one automatically.

        Returns:
            TaskPred: the appended relationship.

        Raises:
            ValueError: on an unknown pred_type, non-numeric lag, unknown
                task, duplicate relationship, or missing project context.
        """
        self._check_type(pred_type)
        lag = self._check_lag(lag_hr_cnt)
        tasks = self._resolve_tasks(tasks)
        if tasks is not None:
            succ = self._find_task(tasks, task_id)
            if succ is None:
                raise ValueError(f"task_id {task_id} not found in the schedule")
            pred = self._find_task(tasks, pred_task_id)
            if pred is None:
                raise ValueError(f"pred_task_id {pred_task_id} not found in the schedule")
            if proj_id is None:
                proj_id = succ.proj_id
            if pred_proj_id is None:
                pred_proj_id = pred.proj_id
        if proj_id is None:
            raise ValueError(
                "proj_id could not be derived — pass proj_id=/pred_proj_id= "
                "or a tasks collection")
        self._check_duplicate(task_id, pred_task_id, pred_type)
        rel = TaskPred.create(
            task_id=task_id, pred_task_id=pred_task_id, pred_type=pred_type,
            lag_hr_cnt=lag, proj_id=proj_id, pred_proj_id=pred_proj_id,
            comments=comments, task_pred_id=self.next_task_pred_id())
        self.task_pred.append(rel)
        return rel

    def remove_relationship(self, rel):
        """Remove a relationship (TaskPred instance or task_pred_id).

        Raises:
            ValueError: if the relationship is not in this collection.
        """
        if isinstance(rel, TaskPred):
            if rel not in self.task_pred:
                raise ValueError("Relationship not found in this collection")
            self.task_pred.remove(rel)
            return rel
        found = self.find_by_id(rel)
        if found is None:
            raise ValueError(f"No relationship with task_pred_id {rel!r}")
        self.task_pred.remove(found)
        return found

    def replace_relationship(self, rel, task_id=None, pred_task_id=None,
                             pred_type=None, lag_hr_cnt=None, comments=None,
                             tasks=None):
        """Atomically re-route a relationship.

        Builds the replacement first (so validation failures leave the
        collection untouched), then swaps it for ``rel`` (TaskPred
        instance or task_pred_id). Unspecified fields are inherited from
        the old relationship.
        """
        old = self.find_by_id(rel) if not isinstance(rel, TaskPred) else rel
        if old is None:
            raise ValueError(f"No relationship with task_pred_id {rel!r}")
        if isinstance(rel, TaskPred) and rel not in self.task_pred:
            raise ValueError("Relationship not found in this collection")
        new = self.add_relationship(
            task_id=old.task_id if task_id is None else task_id,
            pred_task_id=old.pred_task_id if pred_task_id is None else pred_task_id,
            pred_type=old.pred_type if pred_type is None else pred_type,
            lag_hr_cnt=old.lag_hr_cnt if lag_hr_cnt is None else lag_hr_cnt,
            comments=old.comments if comments is None else comments,
            proj_id=old.proj_id,
            pred_proj_id=old.pred_proj_id,
            tasks=tasks)
        self.task_pred.remove(old)
        return new

    @property
    def relations(self) -> List[TaskPred]:
        return self.task_pred

    @property
    def leads(self):
        return list(filter(lambda x: x.lag_hr_cnt < 0 if x.lag_hr_cnt else None, self.task_pred))

    @property
    def finish_to_start(self) -> List[TaskPred]:
        return list(filter(lambda x: x.pred_type == 'PR_FS', self.task_pred))
    
    def get_successors(self, act_id) -> List[TaskPred]:
        succ = list(filter(lambda x: x.pred_task_id == act_id, self.task_pred))
        return succ

    def get_predecessors(self, act_id) -> List[TaskPred]:
        succ = list(filter(lambda x: x.task_id == act_id, self.task_pred))
        return succ

    def count(self):
        return len(self.task_pred)

    def __len__(self):
        return len(self.task_pred)

    def __iter__(self):
        return iter(self.task_pred)

