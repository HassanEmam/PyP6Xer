"""Full DCMA-14 coverage: every check exercised on a crafted schedule.

Fixture schedule (data date 2026-02-01 08:00, calendar 8h/day):
  A (1001) TK_Complete, act dates, target dates        -> required+earned
  B (1002) TK_NotStart, critical (tf=0), future target -> critical chain with D
  C (1003) TK_NotStart, total float 80h                -> check #6 large float
  D (1004) TK_NotStart, tf=-10, CS_MSO, 100h duration  -> #5 #7 #8, critical
  E (1005) TK_Active, act start after data date, act end
           after target end, has resource assignment   -> #9 #10 #11 #14

Relationships: A->B PR_FS lag 8 (check #2), B->D PR_FS lag -8 (check #3
lead, critical chain for #12), C->D PR_SS.
"""
import math

import pytest

from xerparser.reader import Reader
from xerparser.dcma14.analysis import DCMA14

TASK_FIELDS = ("task_id", "proj_id", "wbs_id", "clndr_id", "phys_complete_pct",
               "rev_fdbk_flag", "est_wt", "lock_plan_flag", "auto_compute_act_flag",
               "complete_pct_type", "task_type", "duration_type", "status_code",
               "task_code", "task_name", "rsrc_id", "total_float_hr_cnt",
               "free_float_hr_cnt", "remain_drtn_hr_cnt", "act_work_qty",
               "remain_work_qty", "target_work_qty", "target_drtn_hr_cnt",
               "target_equip_qty", "act_equip_qty", "remain_equip_qty", "cstr_date",
               "act_start_date", "act_end_date", "late_start_date", "late_end_date",
               "expect_end_date", "early_start_date", "early_end_date",
               "restart_date", "reend_date", "target_start_date", "target_end_date",
               "rem_late_start_date", "rem_late_end_date", "cstr_type",
               "priority_type", "suspend_date", "resume_date", "float_path",
               "float_path_order", "guid", "tmpl_guid", "cstr_date2", "cstr_type2",
               "driving_path_flag", "act_this_per_work_qty", "act_this_per_equip_qty",
               "external_early_start_date", "external_late_end_date", "create_date",
               "update_date", "create_user", "update_user", "location_id")

TASKS = [
    # A: complete, earned, required
    {"task_id": "1001", "task_code": "A", "status_code": "TK_Complete",
     "total_float_hr_cnt": "0", "target_drtn_hr_cnt": "8",
     "target_start_date": "2026-01-05 08:00", "target_end_date": "2026-01-06 17:00",
     "act_start_date": "2026-01-05 08:00", "act_end_date": "2026-01-06 17:00",
     "clndr_id": "1", "proj_id": "1"},
    # B: critical, not started, future target (not required)
    {"task_id": "1002", "task_code": "B", "status_code": "TK_NotStart",
     "total_float_hr_cnt": "0", "target_drtn_hr_cnt": "8",
     "target_start_date": "2026-02-10 08:00", "clndr_id": "1", "proj_id": "1"},
    # C: large float
    {"task_id": "1003", "task_code": "C", "status_code": "TK_NotStart",
     "total_float_hr_cnt": "80", "target_drtn_hr_cnt": "8",
     "target_start_date": "2026-02-10 08:00", "clndr_id": "1", "proj_id": "1"},
    # D: hard constraint, negative float, long duration, critical
    {"task_id": "1004", "task_code": "D", "status_code": "TK_NotStart",
     "total_float_hr_cnt": "-10", "target_drtn_hr_cnt": "100",
     "cstr_type": "CS_MSO", "cstr_date": "2026-03-01 08:00",
     "target_start_date": "2026-02-10 08:00", "clndr_id": "1", "proj_id": "1"},
    # E: active, invalid dates, slippage, required+earned, critical
    {"task_id": "1005", "task_code": "E", "status_code": "TK_Active",
     "total_float_hr_cnt": "0", "target_drtn_hr_cnt": "8",
     "target_start_date": "2026-01-20 08:00", "target_end_date": "2026-02-05 17:00",
     "act_start_date": "2026-02-10 08:00",  # after data date -> invalid
     "act_end_date": "2026-02-12 17:00",    # after target end -> slippage
     "early_start_date": "2026-01-01 08:00",  # before data date -> invalid
     "early_end_date": "2026-02-20 17:00",    # after target end -> slippage
     "clndr_id": "1", "proj_id": "1"},
]

PREDS = [
    {"task_pred_id": "1", "task_id": "1002", "pred_task_id": "1001",
     "proj_id": "1", "pred_proj_id": "1", "pred_type": "PR_FS", "lag_hr_cnt": "8"},
    {"task_pred_id": "2", "task_id": "1004", "pred_task_id": "1002",
     "proj_id": "1", "pred_proj_id": "1", "pred_type": "PR_FS", "lag_hr_cnt": "-8"},
    {"task_pred_id": "3", "task_id": "1004", "pred_task_id": "1003",
     "proj_id": "1", "pred_proj_id": "1", "pred_type": "PR_SS"},
]

TASK_FIELDS_LINE = "%F\t" + "\t".join(TASK_FIELDS)


def _task_rows():
    rows = []
    for t in TASKS:
        full = {f: "" for f in TASK_FIELDS}
        full.update(t)
        rows.append("%R\t" + "\t".join(full[f] for f in TASK_FIELDS))
    return rows


def _pred_rows():
    fields = ["task_pred_id", "task_id", "pred_task_id", "proj_id", "pred_proj_id",
              "pred_type", "lag_hr_cnt", "comments", "float_path", "aref", "arls"]
    rows = ["%T\tTASKPRED", "%F\t" + "\t".join(fields)]
    for p in PREDS:
        full = {f: "" for f in fields}
        full.update(p)
        rows.append("%R\t" + "\t".join(full[f] for f in fields))
    return rows


@pytest.fixture(scope="module")
def dcma(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("dcma14")
    rows = ["ERMHDR\t19.12\t2026-01-02\tProject\tjdoe"]
    rows += ["%T\tCALENDAR",
             "%F\tclndr_id\tdefault_flag\tclndr_name\tproj_id\tbase_clndr_id\t"
             "last_chng_date\tclndr_type\tday_hr_cnt\tweek_hr_cnt\tmonth_hr_cnt\t"
             "year_hr_cnt\trsrc_private\tclndr_data",
             "%R\t1\tY\tCal\t\t\t\tCA_Calendar\t8\t40\t172\t2080\tN\t*"]
    rows += ["%T\tPROJECT",
             "%F\tproj_id\tlast_recalc_date\tlast_fin_dates_id\t"
             "last_baseline_update_date",
             "%R\t1\t2026-02-01 08:00\t\t"]  # data date
    rows += ["%T\tPROJWBS",
             "%F\twbs_id\tproj_id\twbs_name",
             "%R\t100\t1\tRoot"]
    rows += ["%T\tTASK", TASK_FIELDS_LINE] + _task_rows()
    rows += _pred_rows()
    rows += ["%T\tTASKRSRC",
             "%F\ttaskrsrc_id\ttask_id\tproj_id\trsrc_id",
             "%R\t9001\t1005\t1\t1"]  # only E has a resource assignment
    rows.append("%E")
    path = tmp / "dcma.xer"
    path.write_text("\n".join(rows) + "\n", encoding="cp1252")
    reader = Reader(str(path))
    return DCMA14(reader).analysis()["analysis"]


class TestCheck1OpenEnds:
    def test_successors(self, dcma):
        ids = {a["id"] for a in dcma["successors"]["activities"] if a}
        assert ids == {"D", "E"}

    def test_predecessors(self, dcma):
        ids = {a["id"] for a in dcma["predecessors"]["activities"] if a}
        assert ids == {"A", "C", "E"}

    def test_counts(self, dcma):
        assert dcma["successors"]["cnt"] == 2
        assert dcma["predecessors"]["cnt"] == 3
        assert dcma["predecessors"]["pct"] == pytest.approx(3 / 5)
        assert dcma["successors"]["pct"] == pytest.approx(2 / 5)


class TestCheck2Lags:
    def test_positive_lag_detected(self, dcma):
        assert dcma["lags"]["cnt"] == 1
        rel = dcma["lags"]["relations"][0]
        assert rel["successor"]["id"] == "B"
        assert rel["predecessor"]["id"] == "A"
        assert rel["lag"] == 1  # 8h / 8h day = 1 day


class TestCheck3Leads:
    def test_negative_lag_detected(self, dcma):
        assert dcma["leads"]["cnt"] == 1
        rel = dcma["leads"]["relations"][0]
        assert rel["successor"]["id"] == "D"
        assert rel["predecessor"]["id"] == "B"


class TestCheck4RelationshipTypes:
    def test_fs_count(self, dcma):
        assert dcma["relations"]["fs_cnt"] == 2

    def test_relationship_entries(self, dcma):
        types = {r["type"] for r in dcma["relations"]["relationship"]}
        assert types == {"PR_FS"}


class TestCheck5Constraints:
    def test_hard_constraint_found(self, dcma):
        assert dcma["constraints"]["cstr_cnt"] == 1
        assert dcma["constraints"]["cstrs"][0]["id"] == "D"


class TestCheck6TotalFloat:
    def test_large_float(self, dcma):
        assert dcma["totalfloat"]["cnt"] == 1
        assert dcma["totalfloat"]["activities"][0]["id"] == "C"


class TestCheck7NegativeFloat:
    def test_negative_float(self, dcma):
        assert dcma["negativefloat"]["cnt"] == 1
        assert dcma["negativefloat"]["activities"][0]["id"] == "D"


class TestCheck8Durations:
    def test_long_duration(self, dcma):
        ids = {a["id"] for a in dcma["duration"]["activities"]}
        assert ids == {"D"}  # 100h / 8h = 12.5 days > 1


class TestCheck9InvalidDates:
    def test_invalid_dates(self, dcma):
        assert dcma["invaliddates"]["cnt"] == 1
        assert {a["id"] for a in dcma["invaliddates"]["actual_start"]} == {"E"}
        assert {a["id"] for a in dcma["invaliddates"]["early_start"]} == {"E"}


class TestCheck10Resources:
    def test_missing_resource_assignments(self, dcma):
        assert dcma["resources"]["cnt"] == 4  # all but E


class TestCheck11Slippage:
    def test_slipped_activity(self, dcma):
        assert dcma["slippage"]["cnt"] == 1
        assert dcma["slippage"]["activities"][0]["id"] == "E"


class TestCheck12CriticalPath:
    def test_critical_activities(self, dcma):
        ids = {a["id"] for a in dcma["critical"]["activities"]}
        assert ids == {"B", "D", "E"}  # A complete, C float 80
        assert dcma["critical"]["cnt"] == 3

    def test_longest_chain(self, dcma):
        assert dcma["critical_test"]["longest_chain_cnt"] == 2  # B -> D
        assert dcma["critical_test"]["passed"] is True


class TestCheck13CPLI:
    def test_cpli_value(self, dcma):
        cp = 100 + 8  # D + B durations in hours
        assert dcma["cpli"]["critical_path_length"] == cp
        assert dcma["cpli"]["total_float"] == 80.0
        assert dcma["cpli"]["cpli"] == pytest.approx(cp / (cp + 80))


class TestCheck14BEI:
    def test_bei(self, dcma):
        assert dcma["bei"]["earned"] == 2  # A and E
        assert dcma["bei"]["required"] == 2  # A and E target_start <= data date
        assert dcma["bei"]["bei"] == pytest.approx(1.0)
