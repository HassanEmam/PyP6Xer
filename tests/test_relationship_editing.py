"""Tests for the relationship editing API (issue #7).

Programmatic re-sequencing of TASKPRED relationships — add, edit,
remove, re-route — with a valid XER written back.
"""
import pytest

from xerparser.reader import Reader
from xerparser.write import writeXER
from xerparser.model.predecessors import Predecessors

from tests.test_review_regressions import TASK_HEADER

TASK_FIELDS = TASK_HEADER

def _sched(path):
    """Schedule with tasks 1001/1002/1003 and one FS rel 1001 -> 1002."""
    rows = ["ERMHDR\t19.12\t2026-01-02\tProject\tjdoe"]
    rows += ["%T\tCALENDAR",
             "%F\tclndr_id\tdefault_flag\tclndr_name\tproj_id\tbase_clndr_id\tlast_chng_date\tclndr_type\tday_hr_cnt\tweek_hr_cnt\tmonth_hr_cnt\tyear_hr_cnt\trsrc_private\tclndr_data",
             "%R\t1\tY\tCal-A\t\t\t\tCA_Calendar\t8\t40\t172\t2080\tN\t*"]
    rows += ["%T\tTASK", "%F\t" + "\t".join(TASK_FIELDS)]
    for tid, name in ((1001, "One"), (1002, "Two"), (1003, "Three")):
        row = {f: "" for f in TASK_FIELDS}
        row.update({"task_id": str(tid), "proj_id": "1", "clndr_id": "1",
                    "task_code": "A" + str(tid), "task_name": name,
                    "total_float_hr_cnt": "0", "free_float_hr_cnt": "0"})
        rows.append("%R\t" + "\t".join(row[f] for f in TASK_FIELDS))
    rows += ["%T\tTASKPRED",
             "%F\ttask_pred_id\ttask_id\tpred_task_id\tproj_id\tpred_proj_id\tpred_type\tlag_hr_cnt\tcomments\tfloat_path\taref\tarls",
             "%R\t1\t1002\t1001\t1\t1\tPR_FS\t8\toriginal\t\t\t"]
    rows.append("%E")
    path.write_text("\n".join(rows) + "\n", encoding="cp1252")
    return path

THREE_TASK_EXTRA = (
    "%T\tTASK\n"
    "%F\t" + "\t".join([
        "task_id", "proj_id", "wbs_id", "clndr_id", "phys_complete_pct", "rev_fdbk_flag",
        "est_wt", "lock_plan_flag", "auto_compute_act_flag", "complete_pct_type", "task_type",
        "duration_type", "status_code", "task_code", "task_name", "rsrc_id",
        "total_float_hr_cnt", "free_float_hr_cnt", "remain_drtn_hr_cnt", "act_work_qty",
        "remain_work_qty", "target_work_qty", "target_drtn_hr_cnt", "target_equip_qty",
        "act_equip_qty", "remain_equip_qty", "cstr_date", "act_start_date", "act_end_date",
        "late_start_date", "late_end_date", "expect_end_date", "early_start_date",
        "early_end_date", "restart_date", "reend_date", "target_start_date",
        "target_end_date", "rem_late_start_date", "rem_late_end_date", "cstr_type",
        "priority_type", "suspend_date", "resume_date", "float_path", "float_path_order",
        "guid", "tmpl_guid", "cstr_date2", "cstr_type2", "driving_path_flag",
        "act_this_per_work_qty", "act_this_per_equip_qty", "external_early_start_date",
        "external_late_end_date", "create_date", "update_date", "create_user",
        "update_user", "location_id"]) + "\n"
    "%R\t1001\t1\t\t1\t0\tN\t1\tN\tN\tCP_Duration\tTT_Task\tDT_Fixed\tTK_NotStart\tA1000\tOne\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n"
    "%R\t1002\t1\t\t1\t0\tN\t1\tN\tN\tCP_Duration\tTT_Task\tDT_Fixed\tTK_NotStart\tA1000\tTwo\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n"
    "%R\t1003\t1\t\t1\t0\tN\t1\tN\tN\tCP_Duration\tTT_Task\tDT_Fixed\tTK_NotStart\tA1000\tThree\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n"
    "%T\tTASKPRED\n"
    "%F\ttask_pred_id\ttask_id\tpred_task_id\tproj_id\tpred_proj_id\tpred_type\tlag_hr_cnt\tcomments\tfloat_path\taref\tarls\n"
    "%R\t1\t1002\t1001\t1\t1\tPR_FS\t8\toriginal\t\t\t\n"
)


@pytest.fixture()
def reader(tmp_path):
    return Reader(_sched(tmp_path / "sched.xer"))


class TestAddRelationship:
    def test_add_fs_relationship(self, reader):
        rel = reader.relations.add_relationship(task_id=1003, pred_task_id=1002)
        assert rel.task_id == 1003 and rel.pred_task_id == 1002
        assert rel.pred_type == "PR_FS" and rel.lag_hr_cnt is None
        assert rel.proj_id == 1 and rel.pred_proj_id == 1
        assert len(reader.relations) == 2

    def test_auto_id_does_not_collide(self, reader):
        rel = reader.relations.add_relationship(task_id=1003, pred_task_id=1002)
        assert rel.task_pred_id == 2  # existing id 1
        rel2 = reader.relations.add_relationship(task_id=1003, pred_task_id=1001,
                                                 pred_type="PR_SS")
        assert rel2.task_pred_id == 3
        # large existing ids are respected
        reader.relations.task_pred[0].task_pred_id = "50000"
        assert reader.relations.next_task_pred_id() == 50001

    def test_cross_project_link(self, reader):
        rel = reader.relations.add_relationship(
            task_id=1003, pred_task_id=1002, pred_proj_id=77)
        assert rel.proj_id == 1 and rel.pred_proj_id == 77

    def test_all_pred_types(self, reader):
        for pt in ("PR_FS", "PR_SS", "PR_FF", "PR_SF"):
            reader.relations.add_relationship(task_id=1003, pred_task_id=1002,
                                              pred_type=pt)

    def test_standalone_collection_with_explicit_ids(self):
        preds = Predecessors()
        rel = preds.add_relationship(task_id=5, pred_task_id=4, proj_id=1,
                                     pred_proj_id=1)
        assert rel.task_id == 5 and rel.task_pred_id == 1


class TestAddValidation:
    def test_bad_pred_type(self, reader):
        with pytest.raises(ValueError, match="pred_type"):
            reader.relations.add_relationship(task_id=1003, pred_task_id=1002,
                                              pred_type="PR_XX")

    def test_bad_lag(self, reader):
        with pytest.raises(ValueError, match="lag_hr_cnt"):
            reader.relations.add_relationship(task_id=1003, pred_task_id=1002,
                                              lag_hr_cnt="soon")

    def test_unknown_task(self, reader):
        with pytest.raises(ValueError, match="task_id 9999"):
            reader.relations.add_relationship(task_id=9999, pred_task_id=1002)

    def test_unknown_predecessor(self, reader):
        with pytest.raises(ValueError, match="pred_task_id 9999"):
            reader.relations.add_relationship(task_id=1002, pred_task_id=9999)

    def test_duplicate_rejected(self, reader):
        with pytest.raises(ValueError, match="already exists"):
            reader.relations.add_relationship(task_id=1002, pred_task_id=1001,
                                              pred_type="PR_FS")

    def test_missing_project_context(self):
        preds = Predecessors()
        with pytest.raises(ValueError, match="proj_id"):
            preds.add_relationship(task_id=5, pred_task_id=4)

    def test_failed_add_leaves_collection_untouched(self, reader):
        n = len(reader.relations)
        with pytest.raises(ValueError):
            reader.relations.add_relationship(task_id=1003, pred_task_id=1002,
                                              lag_hr_cnt="soon")
        assert len(reader.relations) == n


class TestRemoveAndReplace:
    def test_remove_by_object_and_id(self, reader):
        rel = reader.relations.task_pred[0]
        reader.relations.remove_relationship(rel)
        assert len(reader.relations) == 0
        reader.relations.add_relationship(task_id=1003, pred_task_id=1002)
        reader.relations.remove_relationship(1)  # ids restart after the list empties
        assert len(reader.relations) == 0

    def test_remove_missing_raises(self, reader):
        with pytest.raises(ValueError, match="task_pred_id 99"):
            reader.relations.remove_relationship(99)

    def test_replace_reroutes(self, reader):
        new = reader.relations.replace_relationship(
            1, pred_task_id=1003, pred_type="PR_SS", lag_hr_cnt=4.0)
        assert len(reader.relations) == 1
        assert new.task_id == 1002 and new.pred_task_id == 1003
        assert new.pred_type == "PR_SS" and new.lag_hr_cnt == 4.0
        assert new.comments == "original"  # inherited

    def test_replace_by_object(self, reader):
        old = reader.relations.task_pred[0]
        new = reader.relations.replace_relationship(old, task_id=1003)
        assert new.task_id == 1003 and new.pred_task_id == 1001

    def test_replace_missing_raises(self, reader):
        with pytest.raises(ValueError, match="task_pred_id 99"):
            reader.relations.replace_relationship(99, task_id=1002)

    def test_replace_validation_failure_atomic(self, reader):
        """Bad replacement type must not remove the old relationship."""
        with pytest.raises(ValueError, match="pred_type"):
            reader.relations.replace_relationship(1, pred_type="PR_XX")
        assert len(reader.relations) == 1
        assert reader.relations.task_pred[0].pred_type == "PR_FS"


class TestWriteBack:
    def test_edits_survive_round_trip(self, tmp_path):
        r = Reader(_sched(tmp_path / "sched.xer"))
        r.relations.add_relationship(task_id=1003, pred_task_id=1002,
                                     lag_hr_cnt=12.5, comments="resequenced")
        r.relations.replace_relationship(1, pred_type="PR_SS")
        out = tmp_path / "out.xer"
        writeXER(r, out)
        r2 = Reader(out)
        rels = {(rel.task_id, rel.pred_task_id, rel.pred_type): rel
                for rel in r2.relations}
        assert (1002, 1001, "PR_SS") in rels
        assert rels[(1002, 1001, "PR_SS")].comments == "original"
        assert (1003, 1002, "PR_FS") in rels
        assert rels[(1003, 1002, "PR_FS")].lag_hr_cnt == 12.5
        assert rels[(1003, 1002, "PR_FS")].comments == "resequenced"

    def test_removal_survives_round_trip(self, tmp_path):
        r = Reader(_sched(tmp_path / "sched.xer"))
        r.relations.remove_relationship(1)
        out = tmp_path / "out.xer"
        writeXER(r, out)
        r2 = Reader(out)
        assert len(r2.relations) == 0

    def test_tasks_passthroughs(self, reader):
        assert [rel.pred_task_id for rel in reader.activities.get_predecessors(1002)] == [1001]
        assert [rel.task_id for rel in reader.activities.get_successors(1001)] == [1002]
        assert reader.activities.get_predecessors(1003) == []

    def test_dcma_still_runs_after_edit(self, reader):
        reader.relations.add_relationship(task_id=1003, pred_task_id=1002)
        d = __import__("xerparser.dcma14.analysis", fromlist=["DCMA14"]).DCMA14(reader)
        analysis = d.analysis()["analysis"]
        assert analysis["summary"]["relationship_cnt"] == 2
        assert analysis["critical_test"]["longest_chain_cnt"] >= 1
