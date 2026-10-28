"""Tasks query methods on a full Reader."""
import datetime
import sys

import pytest

from xerparser.reader import Reader

sys.path.insert(0, "tests")
from table_fixtures import build_xer, table_params  # noqa: E402

# task_id, task_code, status, float, drtn, target_start, cstr_type
TASKS = [
    ("101", "A", "TK_Complete", "0", "8", "2026-01-05 08:00", ""),
    ("102", "B", "TK_NotStart", "0", "8", "2026-02-10 08:00", ""),
    ("103", "C", "TK_NotStart", "120", "8", "2026-02-10 08:00", "CS_MSO"),
    ("104", "D", "TK_NotStart", "40", "8", "2026-02-10 08:00", ""),
]


def _task_row(tid, code, status, tf, drtn, tstart, cstr):
    vals = {"task_id": tid, "proj_id": "1", "wbs_id": "100", "clndr_id": "1",
            "task_type": "TT_Task", "duration_type": "DT_FixedDrtn",
            "status_code": status, "task_code": code, "task_name": f"Task {code}",
            "total_float_hr_cnt": tf, "target_drtn_hr_cnt": drtn,
            "target_start_date": tstart}
    if cstr:
        vals["cstr_type"] = cstr
        vals["cstr_date"] = "2026-03-01 08:00"
    return vals


@pytest.fixture(scope="module")
def reader(tmp_path_factory):
    tables = {
        "CALENDAR": [table_params("CALENDAR", overrides={"clndr_id": "1",
                                                         "day_hr_cnt": "8"})],
        "TASK": [_task_row(*t) for t in TASKS],
        "TASKPRED": [
            table_params("TASKPRED", overrides={
                "task_pred_id": "1", "task_id": "102", "pred_task_id": "101",
                "pred_type": "PR_FS"}),
            table_params("TASKPRED", overrides={
                "task_pred_id": "2", "task_id": "104", "pred_task_id": "103",
                "pred_type": "PR_SS"}),
        ],
    }
    path = tmp_path_factory.mktemp("queries") / "q.xer"
    build_xer(path, tables)
    return Reader(str(path))


def test_find_by_code(reader):
    assert reader.activities.find_by_code("B").task_id == 102
    assert reader.activities.find_by_code("ZZ") == []


def test_find_by_id(reader):
    assert reader.activities.find_by_id(103).task_code == "C"
    assert reader.activities.find_by_id(999) == []


def test_activities_by_status(reader):
    active = reader.activities.activities_by_status("TK_NotStart")
    assert [t.task_code for t in active] == ["B", "C", "D"]


def test_activities_by_wbs_id(reader):
    assert len(reader.activities.activities_by_wbs_id(100)) == 4
    assert reader.activities.activities_by_wbs_id(999) == []


def test_activities_with_hard_constraints(reader):
    constrained = reader.activities.activities_with_hard_contratints()
    assert len(constrained) == 1
    assert constrained[0].task_code == "C"


def test_activities_by_type_filters_constraints(reader):
    # NOTE: activities_by_type actually filters on cstr_type, not task_type.
    assert [t.task_code for t in reader.activities.activities_by_type("CS_MSO")] == ["C"]
    assert reader.activities.activities_by_type("TT_Task") == []


def test_duration_greater_than(reader):
    # NOTE: compares against target_drtn_hr_cnt, i.e. HOURS not days
    assert len(reader.activities.duration_greater_than(7.5)) == 4
    assert reader.activities.duration_greater_than(8) == []


def test_get_by_project(reader):
    assert len(reader.activities.get_by_project(1)) == 4


def test_constraints(reader):
    c = reader.activities.constraints
    assert len(c) == 1
    assert c[0]["ConstraintType"] == "CS_MSO"


def test_task_totalint(reader):
    c = reader.activities.find_by_code("C")
    assert c.totalint == pytest.approx(15.0)  # 120h / 8h calendar
    a = reader.activities.find_by_code("A")
    assert a.totalint is None  # zero float is falsy -> None


def test_float_ranges(reader):
    # float helpers convert to days using the calendar (8h/day)
    assert [t.task_code for t in reader.activities.float_greater_than(4)] == ["C", "D"]
    # TK_Complete tasks are excluded from float queries
    assert [t.task_code for t in reader.activities.float_less_than(0.5)] == ["B"]
    assert [t.task_code for t in reader.activities.float_within_range(4, 6)] == ["D"]


def test_no_predecessors_and_successors(reader):
    # relations: A(101)->B(102), C(103)->D(104)
    np = reader.activities.no_predecessors()
    assert {t.task_code for t in np} == {"A", "C"}
    ns = reader.activities.no_successors()
    assert {t.task_code for t in ns} == {"B", "D"}


def test_task_constraint_dict(reader):
    c = reader.activities.find_by_code("C")
    assert c.constraints == {"ConstraintType": "CS_MSO",
                             "ConstrintDate": datetime.datetime(2026, 3, 1, 8, 0)}
    assert reader.activities.find_by_code("A").constraints is None


def test_task_start_end_dates(reader):
    a = reader.activities.find_by_code("A")
    assert a.start_date is not None
    d = reader.activities.find_by_code("D")
    assert d.duration == pytest.approx(1.0)  # 8h / 8h calendar
