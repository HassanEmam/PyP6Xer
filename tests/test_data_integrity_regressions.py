from datetime import datetime
from types import SimpleNamespace

from xerparser.dcma14.analysis import DCMA14
from xerparser.model.activitiyresources import ActivityResources
from xerparser.model.classes.data import Data
from xerparser.model.classes.project import Project
from xerparser.model.classes.rsrcrate import ResourceRate
from xerparser.model.classes.rsrcrcat import ResourceCat
from xerparser.model.classes.task import Task
from xerparser.model.classes.taskpred import TaskPred
from xerparser.model.classes.taskrsrc import TaskRsrc
from xerparser.model.nonworks import NonWorks
from xerparser.model.obss import OBSs
from xerparser.model.predecessors import Predecessors
from xerparser.model.rcattypes import RCatTypes
from xerparser.model.rcatvals import RCatVals
from xerparser.model.resources import Resources
from xerparser.model.rolerates import RoleRates
from xerparser.model.roles import Roles
from xerparser.model.rsrccats import ResourceCategories
from xerparser.model.rsrccurves import ResourceCurves
from xerparser.model.rsrcrates import ResourceRates
from xerparser.model.schedoptions import SchedOptions
from xerparser.model.tasks import Tasks
from xerparser.model.udfvalues import UDFValues
from xerparser.reader import Reader


def test_relationship_fields_and_lookup_preserve_external_project_id():
    predecessors = Predecessors()
    predecessors.add(
        {
            "task_pred_id": "900",
            "task_id": "20",
            "pred_task_id": "10",
            "proj_id": "2",
            "pred_proj_id": "1",
            "pred_type": "PR_FS",
        }
    )

    relationship = predecessors.find_by_id("900")

    assert isinstance(relationship, TaskPred)
    assert relationship.proj_id == 2
    assert relationship.pred_proj_id == 1


def test_resource_parent_and_role_rate_collection_lookups():
    resources = Resources()
    resources.add({"rsrc_id": "1", "rsrc_name": "Parent"})
    resources.add(
        {"rsrc_id": "2", "parent_rsrc_id": "1", "rsrc_name": "Child"}
    )
    assert resources.get_parent(2) is resources.get_resource_by_id(1)
    assert resources.get_parent(1) is None
    assert resources.get_parent(999) is None

    roles = Roles()
    roles.add({"role_id": "10", "role_name": "Planner"})
    assert roles.find_by_id(10).role_name == "Planner"

    role_rates = RoleRates()
    role_rates.add({"role_rate_id": "100", "role_id": "10"})
    role_rates.add({"role_rate_id": "101", "role_id": "10"})
    assert len(role_rates) == 2
    assert role_rates.find_by_id(101).role_id == 10


def test_collection_find_by_id_uses_each_models_actual_identifier():
    cases = [
        (NonWorks(), {"nonwork_type_id": "1"}, "1"),
        (OBSs(), {"obs_id": "2"}, 2),
        (RCatTypes(), {"rsrc_catg_type_id": "3"}, 3),
        (RCatVals(), {"rsrc_catg_id": "4"}, "4"),
        (ResourceCurves(), {"curv_id": "5", "curv_name": "Curve"}, 5),
        (ResourceRates(), {"rsrc_rate_id": "6", "rsrc_id": "60"}, "6"),
        (SchedOptions(), {"schedoptions_id": "7"}, "7"),
        (UDFValues(), {"udf_type_id": "8", "fk_id": "80"}, "8"),
        (
            ResourceCategories(),
            {"rsrc_id": "9", "rsrc_catg_type_id": "90", "rsrc_catg_id": "91"},
            9,
        ),
    ]

    for collection, params, identifier in cases:
        collection.add(params)
        result = collection.find_by_id(identifier)
        assert result is not None
        assert result is list(collection)[0]


def test_resource_assignment_and_project_fields_use_matching_source_columns():
    assignment = TaskRsrc(
        {"act_this_per_cost": "100.0", "act_this_per_qty": "5.0"}
    )
    assert assignment.act_this_per_cost == "100.0"
    assert assignment.act_this_per_qty == "5.0"

    assignments = ActivityResources()
    assignments.add({"taskrsrc_id": "1", "task_id": "2"}, Data())
    assert len(assignments) == 1

    project = Project(
        {
            "proj_id": "1",
            "last_fin_dates_id": "77",
            "last_baseline_update_date": "2026-08-01 00:00",
        },
        Data(),
    )
    assert project.last_fin_dates_id == "77"
    assert project.last_baseline_update_date == "2026-08-01 00:00"

    task = Task(
        {"task_id": "2", "float_path": "3", "float_path_order": "4"}, Data()
    )
    assert task.float_path == "3"
    assert task.float_path_order == "4"
    assert task.int_path == "3"
    assert task.int_path_order == "4"

    options = SchedOptions()
    options.add(
        {
            "schedoptions_id": "9",
            "key_activity_for_multiple_longest_paths": "A1000",
        }
    )
    assert options.find_by_id("9").key_activity_for_multiple_longest_paths == "A1000"

    curves = ResourceCurves()
    curves.add({"curv_id": "50"})
    assert curves.find_by_id(50).curv_name is None

    resource_rate = ResourceRate(
        {"rsrc_rate_id": "unique-rate", "rsrc_id": "unique-resource"}
    )
    assert ResourceRate.find_by_resource_id("unique-resource") is resource_rate


def test_reader_writer_round_trip_preserves_role_and_resource_category_tables(tmp_path):
    source = tmp_path / "source.xer"
    source.write_text(
        "\n".join(
            [
                "ERMHDR\t8.0\t2026-08-19",
                "%T\tROLE",
                "%F\trole_id\tparent_role_id\tseq_num\trole_name\trole_short_name\tpobs_id\tdef_cost_qty_link_flag\tcost_qty_type\trole_descr\tlast_checksum",
                "%R\t10\t\t1\tPlanner\tPLN\t\tY\tQT_Hour\tPlanning role\trole-checksum",
                "%T\tROLERATE",
                "%F\trole_rate_id\trole_id\tcost_per_qty\tcost_per_qty2\tcost_per_qty3\tcost_per_qty4\tcost_per_qty5",
                "%R\t100\t10\t100\t\t\t\t",
                "%R\t101\t10\t110\t\t\t\t",
                "%T\tRCATTYPE",
                "%F\trsrc_catg_type_id\tseq_num\trsrc_catg_short_len\trsrc_catg_type",
                "%R\t20\t1\t20\tDiscipline",
                "%T\tRCATVAL",
                "%F\trsrc_catg_id\trsrc_catg_type_id\trsrc_catg_short_name\trsrc_catg_name\tparent_rsrc_catg_id",
                "%R\t30\t20\tCIV\tCivil\t",
                "%T\tRSRC",
                "%F\trsrc_id\tparent_rsrc_id\trsrc_name\tlevel_flag\tlast_checksum",
                "%R\t1\t\tEngineer\tN\tresource-checksum",
                "%T\tRSRCRCAT",
                "%F\trsrc_id\trsrc_catg_type_id\trsrc_catg_id",
                "%R\t1\t20\t30",
                "%E",
                "",
            ]
        ),
        encoding="utf-8",
    )

    reader = Reader(str(source))
    assert len(reader.roles) == 1
    assert len(reader.rolerates) == 2
    assert len(reader.rcattypes) == 1
    assert len(reader.rcatvals) == 1
    assert len(reader.resourcecategories) == 1
    assert reader.roles.find_by_id(10).last_checksum == "role-checksum"
    assert reader.resources.get_resource_by_id(1).last_checksum == "resource-checksum"
    assert reader.resourcecategories.find_by_id(1).rsrc_catg_id == 30

    output = tmp_path / "round-trip.xer"
    reader.write(str(output))
    written = output.read_text(encoding="utf-8")
    for table in ("ROLE", "ROLERATE", "RCATTYPE", "RCATVAL", "RSRCRCAT"):
        assert f"%T\t{table}" in written

    reread = Reader(str(output))
    assert len(reread.roles) == 1
    assert len(reread.rolerates) == 2
    assert len(reread.rcattypes) == 1
    assert len(reread.rcatvals) == 1
    assert len(reread.resourcecategories) == 1
    assert reread.resourcecategories.find_by_id(1).rsrc_catg_id == 30
    assert reread.roles.find_by_id(10).last_checksum == "role-checksum"
    assert reread.resources.get_resource_by_id(1).last_checksum == "resource-checksum"


def test_task_relationship_queries_are_scoped_to_the_reader_data():
    original_relationships = list(TaskPred.obj_list)
    TaskPred.obj_list.clear()
    try:
        first_data = Data()
        first_data.predecessors = Predecessors()
        first_tasks = Tasks()
        first_tasks.add({"task_id": "1", "task_code": "A"}, first_data)
        first_tasks.add({"task_id": "2", "task_code": "B"}, first_data)
        first_data.predecessors.add(
            {"task_pred_id": "1", "task_id": "2", "pred_task_id": "1"}
        )

        second_data = Data()
        second_data.predecessors = Predecessors()
        second_tasks = Tasks()
        second_tasks.add({"task_id": "1", "task_code": "A"}, second_data)
        second_tasks.add({"task_id": "2", "task_code": "B"}, second_data)

        assert {task.task_id for task in second_tasks.has_no_successor} == {1, 2}
        assert {task.task_id for task in second_tasks.has_no_predecessor} == {1, 2}
    finally:
        TaskPred.obj_list[:] = original_relationships


class _Activities:
    def __init__(self, activities, relations):
        self.activities = activities
        self._relations = relations

    def __len__(self):
        return len(self.activities)

    def __iter__(self):
        return iter(self.activities)

    def find_by_id(self, task_id):
        return next(
            (task for task in self.activities if task.task_id == task_id), []
        )

    @property
    def has_no_successor(self):
        predecessor_ids = {relation.pred_task_id for relation in self._relations}
        return [
            task for task in self.activities if task.task_id not in predecessor_ids
        ]

    @property
    def has_no_predecessor(self):
        successor_ids = {relation.task_id for relation in self._relations}
        return [task for task in self.activities if task.task_id not in successor_ids]


class _Assignments:
    def find_by_activity_id(self, task_id):
        return []


def _dcma_programme(tasks, relations):
    return SimpleNamespace(
        activities=_Activities(tasks, relations),
        relations=relations,
        projects=[SimpleNamespace(proj_id=1, last_recalc_date="2026-08-01 00:00")],
        activityresources=_Assignments(),
    )


def _dcma_task(task_id, constraint_type=None):
    return SimpleNamespace(
        task_id=task_id,
        proj_id=1,
        task_code=f"A{task_id}",
        task_name=f"Activity {task_id}",
        duration=1.0,
        total_float_hr_cnt=0.0,
        cstr_type=constraint_type,
        act_start_date=None,
        act_end_date=None,
        early_start_date=None,
        early_end_date=None,
        target_end_date=None,
    )


def test_dcma14_handles_schedules_without_relationships():
    relations = Predecessors()
    results = DCMA14(_dcma_programme([_dcma_task(1)], relations)).analysis()

    assert results["analysis"]["lags"]["pct"] == 0.0
    assert results["analysis"]["leads"]["pct"] == 0.0
    assert results["analysis"]["slippage"]["cnt"] == 0

    empty_results = DCMA14(_dcma_programme([], Predecessors())).analysis()
    assert empty_results["analysis"]["successors"]["pct"] == 0.0
    assert empty_results["analysis"]["critical"]["pct"] == 0.0


def test_dcma14_recognizes_hard_constraints_and_missing_target_dates():
    relations = Predecessors()
    relations.add(
        {
            "task_pred_id": "1",
            "task_id": "2",
            "pred_task_id": "1",
            "pred_type": "PR_FS",
            "lag_hr_cnt": "0",
        }
    )
    tasks = [_dcma_task(1, "CS_MSO"), _dcma_task(2, "CS_MEO")]
    tasks[0].early_end_date = datetime(2026, 8, 2)

    results = DCMA14(_dcma_programme(tasks, relations)).analysis()

    assert results["analysis"]["constraints"]["cstr_cnt"] == 2
    assert results["analysis"]["slippage"]["cnt"] == 0
