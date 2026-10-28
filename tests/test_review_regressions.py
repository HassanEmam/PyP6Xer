"""Regression tests for the full-library review findings.

Each test corresponds to a defect found by reviewing PyP6Xer against the
Oracle P6 XER data map (correctness, spec compliance, robustness).
"""
import pytest

from xerparser.reader import Reader
from xerparser.write import writeXER
from xerparser.model.classes.taskpred import TaskPred
from xerparser.model.classes.wbs import WBS
from xerparser.model.classes.calendar import Calendar
from xerparser.dcma14.analysis import DCMA14


TASK_HEADER = (
    "task_id proj_id wbs_id clndr_id phys_complete_pct rev_fdbk_flag est_wt "
    "lock_plan_flag auto_compute_act_flag complete_pct_type task_type "
    "duration_type status_code task_code task_name rsrc_id "
    "total_float_hr_cnt free_float_hr_cnt remain_drtn_hr_cnt act_work_qty "
    "remain_work_qty target_work_qty target_drtn_hr_cnt target_equip_qty "
    "act_equip_qty remain_equip_qty cstr_date act_start_date act_end_date "
    "late_start_date late_end_date expect_end_date early_start_date "
    "early_end_date restart_date reend_date target_start_date "
    "target_end_date rem_late_start_date rem_late_end_date cstr_type "
    "priority_type suspend_date resume_date float_path float_path_order "
    "guid tmpl_guid cstr_date2 cstr_type2 driving_path_flag "
    "act_this_per_work_qty act_this_per_equip_qty external_early_start_date "
    "external_late_end_date create_date update_date create_user update_user "
    "location_id"
).split()

TASK_ROW = [
    "1001", "1", None, "1", "0", "N", "1", "N", "N", "CP_Duration",
    "TT_Task", "DT_Fixed", "TK_NotStart", "A1000", "Café — naïve résumé",
    None, "40", "0", "16", None, None, None, "16", None, None, None,
    None, None, None, None, None, None, None, None, None, None,
    "2026-01-05 08:00", "2026-01-06 17:00", None, None, "CS_MSO", None,
    None, None, "LT_Path_1", "2", None, None, None, None, "0",
    None, None, None, None, None, None, None, None, None,
]


def _xer(path, extra_tables="", task_row=None, task_header=None, blank_tail=False):
    """Write a minimal CP1252 XER file with one task (+ optional extra tables)."""
    rows = ["ERMHDR\t19.12\t2026-01-02\tProject\tjdoe\tPrimavera\tJohn Doe\tdbx\tProject Management\tUSD"]
    rows += ["%T\tCALENDAR",
             "%F\tclndr_id\tdefault_flag\tclndr_name\tproj_id\tbase_clndr_id\tlast_chng_date\tclndr_type\tday_hr_cnt\tweek_hr_cnt\tmonth_hr_cnt\tyear_hr_cnt\trsrc_private\tclndr_data",
             "%R\t1\tY\tCal-A\t\t\t\tCA_Calendar\t8\t40\t172\t2080\tN\t*"]
    if extra_tables:
        rows += extra_tables.splitlines()
    rows += ["%T\tTASK", "%F\t" + "\t".join(task_header or TASK_HEADER),
             "%R\t" + "\t".join("" if v is None else v for v in (task_row or TASK_ROW)),
             "%T\tTASKPRED",
             "%F\ttask_pred_id\ttask_id\tpred_task_id\tproj_id\tpred_proj_id\tpred_type\tlag_hr_cnt\tcomments\tfloat_path\taref\tarls",
             "%R\tP1\t1001\t1001\t1\t99\tPR_FS\t8\t\t\t\t"]
    rows.append("%E")
    if blank_tail:
        rows.append("")
        rows.append("")
    path.write_text("\n".join(rows) + "\n", encoding="cp1252")
    return path




class TestReaderRobustness:
    def test_cp1252_text_preserved(self, tmp_path):
        """C1: non-ASCII text in ANSI exports must not be deleted."""
        r = Reader(_xer(tmp_path / "one.xer"))
        assert r.activities.activities[0].task_name == "Café — naïve résumé"

    def test_trailing_blank_lines(self, tmp_path):
        """C2: blank/trailing-newline rows must be skipped, not IndexError."""
        r = Reader(_xer(tmp_path / "blank.xer", blank_tail=True))
        assert r.activities.count == 1

    def test_short_row_schema_drift(self, tmp_path):
        """M4: rows shorter than their header (older schemas) must not crash."""
        extra = ("%T\tPROJWBS\n"
                 "%F\twbs_id\tproj_id\twbs_name\twbs_short_name\n"
                 "%R\t10\t1\tRoot")
        r = Reader(_xer(tmp_path / "short.xer", extra_tables=extra))
        assert r.activities.count == 1

    def test_no_cross_file_leak(self, tmp_path):
        """C3: class-level registries must not resolve file B against file A."""
        one = _xer(tmp_path / "one.xer")
        text = one.read_text(encoding="cp1252")
        two = tmp_path / "two.xer"
        two.write_text(
            text.replace("Cal-A", "Other Cal").replace("\t1001\t", "\t2001\t"),
            encoding="cp1252")
        r1, r2 = Reader(one), Reader(two)
        assert r2.activities.activities[0].calendar.clndr_name == "Other Cal"
        assert r1.activities.activities[0].calendar.clndr_name == "Cal-A"

    def test_large_fields(self, tmp_path):
        """Issue #15: clndr_data can exceed the default 128 KiB csv field limit."""
        big = "*" * (200 * 1024)
        extra = ("%T\tCALENDAR\n"
                 "%F\tclndr_id\tdefault_flag\tclndr_name\tproj_id\tbase_clndr_id\t"
                 "last_chng_date\tclndr_type\tday_hr_cnt\tweek_hr_cnt\t"
                 "month_hr_cnt\tyear_hr_cnt\trsrc_private\tclndr_data\n"
                 f"%R\t2\tY\tBigCal\t\t\t\tCA_Calendar\t8\t40\t172\t2080\tN\t{big}")
        r = Reader(_xer(tmp_path / "big.xer", extra_tables=extra))
        assert "BigCal" in [c.clndr_name for c in r.calendars]

    def test_ermhdr_captured(self, tmp_path):
        r = Reader(_xer(tmp_path / "one.xer"))
        assert isinstance(r.xer_header, list)
        assert r.xer_header[0] == "ERMHDR"
        assert r.xer_header[6] == "John Doe"


class TestSpecFieldNames:
    def test_float_path_parsed(self, tmp_path):
        """int_path/float_path: spec names must be read (pre-v19 fallback ok)."""
        r = Reader(_xer(tmp_path / "one.xer"))
        t = r.activities.activities[0]
        assert t.float_path == "LT_Path_1"
        assert t.float_path_order == "2"

    def test_pred_proj_id_from_own_column(self, tmp_path):
        """taskpred.py read pred_proj_id from proj_id."""
        r = Reader(_xer(tmp_path / "one.xer"))
        pred = r.relations.task_pred[0]
        assert pred.pred_proj_id == 99
        assert pred.pred_proj_id != pred.proj_id

    def test_m_constraint_detected(self, tmp_path):
        """DCMA #5: valid hard-constraint codes must not be silently ignored."""
        cstrs = DCMA14(Reader(_xer(tmp_path / "one.xer"))).analysis()['analysis']['constraints']['cstrs']
        assert len(cstrs) == 1

    def test_totalint_uses_calendar_hours(self, tmp_path):
        r = Reader(_xer(tmp_path / "one.xer"))
        t = r.activities.activities[0]
        assert abs(t.totalint - 40 / 8.0) < 1e-9

    def test_tasks_iterable_twice(self, tmp_path):
        """One-shot __iter__ made second iteration empty."""
        r = Reader(_xer(tmp_path / "one.xer"))
        assert len(list(r.activities)) == 1
        assert len(list(r.activities)) == 1

    def test_class_registries_reset_between_files(self, tmp_path):
        one = _xer(tmp_path / "one.xer")
        Reader(one)
        n_pred, n_wbs, n_cal = len(TaskPred.obj_list), len(WBS.obj_list), len(Calendar.obj_list)
        Reader(_xer(tmp_path / "two.xer"))
        assert len(TaskPred.obj_list) == n_pred
        assert len(WBS.obj_list) == n_wbs
        assert len(Calendar.obj_list) == n_cal


class TestWriter:
    def test_emits_spec_tables_and_header(self, tmp_path):
        """Writer must not silently drop tables or fabricate a new ERMHDR."""
        extra = (
            "%T\tROLES\n"
            "%F\trole_id\tparent_role_id\tseq_num\trole_name\trole_short_name\tpobs_id\tdef_cost_qty_link_flag\tcost_qty_type\trole_descr\tlast_checksum\n"
            "%R\t101\t\t1\tEngineer\tENG\t\tY\tPT_RegHrs\t\tchk123\n"
            "%T\tRCATTYPE\n"
            "%F\trsrc_catg_type_id\tseq_num\trsrc_catg_short_len\trsrc_catg_type\tsuper_flag\n"
            "%R\t10\t1\t10\tSkill\tN\n"
            "%T\tRCATVAL\n"
            "%F\trsrc_catg_id\trsrc_catg_type_id\trsrc_catg_short_name\trsrc_catg_name\tparent_rsrc_catg_id\tseq_num\n"
            "%R\t11\t10\tSR\tSenior\t\t2\n"
            "%T\tROLERATE\n"
            "%F\trole_rate_id\trole_id\tcost_per_qty\tcost_per_qty2\tcost_per_qty3\tcost_per_qty4\tcost_per_qty5\n"
            "%R\t201\t101\t75\t\t\t\t\n"
            "%T\tRSRCRCAT\n"
            "%F\trsrc_id\trsrc_catg_type_id\trsrc_catg_id\n"
            "%R\t1\t10\t11\n"
        )
        src = _xer(tmp_path / "one.xer", extra_tables=extra)
        r = Reader(src)
        out = tmp_path / "out.xer"
        writeXER(r, out)
        text = out.read_text()
        tables = {l.split("\t")[1] for l in text.splitlines() if l.startswith("%T")}
        assert {"ROLES", "ROLERATE", "RCATTYPE", "RCATVAL", "RSRCRCAT"} <= tables
        assert "19.12" in text and "John Doe" in text  # ERMHDR round-trips

    def test_round_trip_reparse(self, tmp_path):
        src = _xer(tmp_path / "one.xer")
        r = Reader(src)
        out = tmp_path / "out.xer"
        writeXER(r, out)
        r2 = Reader(out)
        assert r2.activities.count == 1
        assert r2.activities.activities[0].float_path == "LT_Path_1"


class TestSpecFieldsRoundTrip:
    """Fields added for full Oracle data-map compliance must survive write."""

    SPEC_TABLES = {
        "ACTVTYPE": (
            ["actv_code_type_id", "actv_code_type", "actv_code_type_scope", "actv_short_len", "proj_id", "seq_num", "super_flag"],
            {"actv_code_type_id": "7", "actv_code_type": "Phase", "actv_code_type_scope": "PK_PROJECT", "actv_short_len": "10", "proj_id": "1", "seq_num": "1", "super_flag": "Y"},
        ),
        "PCATTYPE": (
            ["proj_catg_type_id", "seq_num", "proj_catg_short_len", "proj_catg_type", "max_proj_catg_wt", "proj_catg_type_wt", "super_flag"],
            {"proj_catg_type_id": "8", "seq_num": "1", "proj_catg_short_len": "10", "proj_catg_type": "Region", "max_proj_catg_wt": "100", "proj_catg_type_wt": "50", "super_flag": "N"},
        ),
        "PCATVAL": (
            ["proj_catg_id", "proj_catg_type_id", "proj_catg_short_name", "proj_catg_name", "parent_proj_catg_id", "seq_num", "proj_catg_wt"],
            {"proj_catg_id": "9", "proj_catg_type_id": "8", "proj_catg_short_name": "EU", "proj_catg_name": "Europe", "parent_proj_catg_id": "", "seq_num": "1", "proj_catg_wt": "75.5"},
        ),
        "RCATTYPE": (
            ["rsrc_catg_type_id", "seq_num", "rsrc_catg_short_len", "rsrc_catg_type", "super_flag"],
            {"rsrc_catg_type_id": "10", "seq_num": "1", "rsrc_catg_short_len": "10", "rsrc_catg_type": "Skill", "super_flag": "N"},
        ),
        "RCATVAL": (
            ["rsrc_catg_id", "rsrc_catg_type_id", "rsrc_catg_short_name", "rsrc_catg_name", "parent_rsrc_catg_id", "seq_num"],
            {"rsrc_catg_id": "11", "rsrc_catg_type_id": "10", "rsrc_catg_short_name": "SR", "rsrc_catg_name": "Senior", "parent_rsrc_catg_id": "", "seq_num": "2"},
        ),
        "PROJECT": (
            ["proj_id", "last_recalc_date", "last_fin_dates_id", "last_baseline_update_date", "checkout_date", "checkout_user_id", "chng_eff_cmp_pct_flag", "control_updates_flag", "hist_interval", "hist_level", "intg_proj_type", "last_level_date", "last_schedule_date", "msp_managed_flag", "px_enable_publication_flag", "px_last_update_date", "px_priority", "risk_level", "sum_data_date", "sum_only_flag", "ts_rsrc_vs_inact_actv_flag"],
            {"proj_id": "1", "checkout_user_id": "jdoe", "hist_interval": "WEEK", "risk_level": "HIGH", "sum_only_flag": "N"},
        ),
        "PROJWBS": (
            ["wbs_id", "proj_id", "obs_id", "seq_num", "est_wt", "proj_node_flag", "sum_data_flag", "status_code", "wbs_short_name", "wbs_name", "phase_id", "parent_wbs_id", "ev_user_pct", "ev_etc_user_value", "orig_cost", "indep_remain_total_cost", "ann_dscnt_rate_pct", "dscnt_period_type", "indep_remain_work_qty", "anticip_start_date", "anticip_end_date", "ev_compute_type", "ev_etc_compute_type", "guid", "tmpl_guid", "plan_open_state", "status_reviewer"],
            {"wbs_id": "100", "proj_id": "1", "seq_num": "1", "proj_node_flag": "Y", "sum_data_flag": "Y", "status_code": "A", "wbs_short_name": "ROOT", "wbs_name": "Root WBS", "status_reviewer": "jdoe"},
        ),
        "RSRC": (
            ["rsrc_id", "parent_rsrc_id", "clndr_id", "rsrc_name", "rsrc_short_name", "rsrc_type", "rsrc_notes", "cost_qty_type", "ot_flag", "active_flag", "guid", "role_id", "shift_id", "user_id", "unit_id", "email_addr", "employee_code", "office_phone", "other_phone", "loc_name", "rsrc_title_name", "rsrc_seq_num", "def_qty_per_hr", "ot_factor", "def_cost_qty_link_flag", "auto_compute_act_flag", "def_cost_per_qty", "location_id", "timesheet_flag", "ts_approve_user_id", "xfer_complete_day_cnt", "xfer_notstart_day_cnt"],
            {"rsrc_id": "1", "clndr_id": "1", "rsrc_name": "Alice", "rsrc_short_name": "AL", "rsrc_type": "RT_Master", "cost_qty_type": "PT_RegHrs", "active_flag": "Y", "timesheet_flag": "Y", "ts_approve_user_id": "jdoe", "xfer_complete_day_cnt": "2", "xfer_notstart_day_cnt": "3"},
        ),
        "TASK": (
            None,  # uses the module TASK_HEADER
            {"task_id": "1001", "proj_id": "1", "wbs_id": "100", "clndr_id": "1", "target_start_date": "2026-01-05 08:00", "target_end_date": "2026-01-06 17:00", "target_drtn_hr_cnt": "16", "review_end_date": "2026-02-01 08:00", "review_type": "LT"},
        ),
        "TASKRSRC": (
            ["taskrsrc_id", "task_id", "proj_id", "cost_qty_link_flag", "role_id", "acct_id", "rsrc_id", "pobs_id", "skill_level", "remain_qty", "target_qty", "remain_qty_per_hr", "target_lag_drtn_hr_cnt", "target_qty_per_hr", "act_ot_qty", "act_reg_qty", "relag_drtn_hr_cnt", "ot_factor", "cost_per_qty", "target_cost", "act_reg_cost", "act_ot_cost", "remain_cost", "act_start_date", "act_end_date", "restart_date", "reend_date", "target_start_date", "target_end_date", "rem_late_start_date", "rem_late_end_date", "rollup_dates_flag", "target_crv", "remain_crv", "actual_crv", "ts_pend_act_end_flag", "guid", "rate_type", "act_this_per_cost", "act_this_per_qty", "curv_id", "rsrc_type", "cost_per_qty_source_type", "create_user", "create_date", "cbs_id", "has_rsrchours", "taskrsrc_sum_id", "pend_act_ot_qty", "pend_act_reg_qty", "pend_complete_pct", "pend_remain_qty", "prior_ts_act_of_qty", "prior_ts_act_reg_qty"],
            {"taskrsrc_id": "5001", "task_id": "1001", "proj_id": "1", "cost_qty_link_flag": "Y", "rsrc_id": "1", "target_qty": "16", "remain_qty": "8", "target_qty_per_hr": "1", "target_start_date": "2026-01-05 08:00", "target_end_date": "2026-01-06 17:00", "target_cost": "800", "cost_per_qty": "50", "rate_type": "RT_Reg", "act_this_per_cost": "100", "act_this_per_qty": "12.25", "create_user": "jdoe", "create_date": "2026-01-02 08:00", "pend_act_ot_qty": "1.5", "pend_act_reg_qty": "2.5", "pend_complete_pct": "25", "pend_remain_qty": "4", "prior_ts_act_of_qty": "3.5", "prior_ts_act_reg_qty": "7.25"},
        ),
    }

    # (collection attr path, object index, field -> expected)
    READBACK = [
        ("acttypes._activitytypes", 0, {"super_flag": "Y"}),
        ("pcattypes._pcattypes", 0, {"max_proj_catg_wt": "100", "super_flag": "N"}),
        ("pcatvals._PCatVals", 0, {"proj_catg_wt": "75.5"}),
        ("rcattypes._rcattypes", 0, {"super_flag": "N"}),
        ("rcatvals._rcatvals", 0, {"seq_num": "2"}),
        ("_projects._projects", 0, {"risk_level": "HIGH", "checkout_user_id": "jdoe"}),
        ("wbss._wbss", 0, {"status_reviewer": "jdoe"}),
        ("resources._rsrcs", 0, {"timesheet_flag": "Y", "ts_approve_user_id": "jdoe", "xfer_notstart_day_cnt": "3"}),
        ("activities.activities", 0, {"review_type": "LT", "review_end_date": "2026-02-01 08:00"}),
        ("activityresources._taskrsrc", 0, {"pend_act_ot_qty": "1.5", "pend_complete_pct": "25", "prior_ts_act_reg_qty": "7.25"}),
    ]

    def _build_spec_xer(self, path):
        rows = ["ERMHDR\t19.12\t2026-01-02\tProject\tjdoe"]
        for table, (header, values) in self.SPEC_TABLES.items():
            fields = header if header is not None else TASK_HEADER + ["review_end_date", "review_type"]
            rows.append("%T\t" + table)
            rows.append("%F\t" + "\t".join(fields))
            rows.append("%R\t" + "\t".join(values.get(f, "") for f in fields))
        rows.append("%T\tCALENDAR")
        rows.append("%F\tclndr_id\tdefault_flag\tclndr_name\tproj_id\tbase_clndr_id\tlast_chng_date\tclndr_type\tday_hr_cnt\tweek_hr_cnt\tmonth_hr_cnt\tyear_hr_cnt\trsrc_private\tclndr_data")
        rows.append("%R\t1\tY\tCal\t\t\t\tCA_Calendar\t8\t40\t172\t2080\tN\t*")
        rows.append("%E")
        path.write_text("\n".join(rows) + "\n", encoding="cp1252")
        return path

    def test_new_fields_parse(self, tmp_path):
        r = Reader(self._build_spec_xer(tmp_path / "spec.xer"))
        for attr, idx, expected in self.READBACK:
            obj = r
            for part in attr.split("."):
                obj = getattr(obj, part)
            for field, want in expected.items():
                assert getattr(obj[idx], field) == want, f"{attr}[{idx}].{field}"

    def test_header_row_alignment_on_write(self, tmp_path):
        r = Reader(self._build_spec_xer(tmp_path / "spec.xer"))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        lines = out.read_text().splitlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("%T\t"):
                n_fields = len(lines[i + 1].split("\t")) - 1
                j = i + 2
                while j < len(lines) and lines[j].startswith("%R"):
                    assert len(lines[j].split("\t")) - 1 == n_fields, \
                        f"misaligned {lines[i]} row {j}"
                    j += 1
                i = j
            else:
                i += 1

    def test_round_trip_preserves_new_fields(self, tmp_path):
        r = Reader(self._build_spec_xer(tmp_path / "spec.xer"))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        r2 = Reader(out)
        for attr, idx, expected in self.READBACK:
            obj = r2
            for part in attr.split("."):
                obj = getattr(obj, part)
            for field, want in expected.items():
                assert getattr(obj[idx], field) == want, f"{attr}[{idx}].{field} after round-trip"


class TestDCMA14Stability:
    def test_full_analysis_no_crash(self, tmp_path):
        d = DCMA14(Reader(_xer(tmp_path / "one.xer"))).analysis()["analysis"]
        assert all(k in d for k in (
            "successors", "lags", "leads", "relations", "constraints",
            "totalfloat", "negativefloat", "duration", "invaliddates",
            "resources", "slippage", "critical", "critical_test", "cpli", "bei"))

    def test_critical_chain_dfs(self):
        """Check #12: longest critical chain via DFS (was unimplemented/0)."""
        from types import SimpleNamespace
        t1 = SimpleNamespace(task_id=1)
        t2 = SimpleNamespace(task_id=2)
        t3 = SimpleNamespace(task_id=3)
        rels = [
            SimpleNamespace(task_id=2, pred_task_id=1, pred_type="PR_FS"),
            SimpleNamespace(task_id=3, pred_task_id=2, pred_type="PR_FS"),
        ]
        d = DCMA14.__new__(DCMA14)
        d.programme = SimpleNamespace(relations=rels)
        chain = d._longest_critical_chain([t1, t2, t3])
        assert [t.task_id for t in chain] == [3, 2, 1]

    def test_critical_chain_cycle_fallback(self):
        """Check #12 must not hang or crash when critical activities form a cycle."""
        from types import SimpleNamespace
        t1 = SimpleNamespace(task_id=1)
        t2 = SimpleNamespace(task_id=2)
        rels = [
            SimpleNamespace(task_id=1, pred_task_id=2, pred_type="PR_FS"),
            SimpleNamespace(task_id=2, pred_task_id=1, pred_type="PR_FS"),
        ]
        d = DCMA14.__new__(DCMA14)
        d.programme = SimpleNamespace(relations=rels)
        chain = d._longest_critical_chain([t1, t2])
        assert len(chain) == 2  # fallback returns the critical set

    def test_critical_chain_needs_fs_type(self):
        """Non-FS relationships do not extend the chain."""
        from types import SimpleNamespace
        t1 = SimpleNamespace(task_id=1)
        t2 = SimpleNamespace(task_id=2)
        rels = [SimpleNamespace(task_id=2, pred_task_id=1, pred_type="PR_SS")]
        d = DCMA14.__new__(DCMA14)
        d.programme = SimpleNamespace(relations=rels)
        chain = d._longest_critical_chain([t1, t2])
        assert len(chain) == 1


class TestRsrcCurv:
    """RSRCCURV (resource curve definitions) — previously rows were silently dropped."""

    CURV_EXTRA = (
        "%T\tRSRCCURV\n"
        "%F\tcurv_data\tcurv_id\tcurv_name\tdefault_flag\n"
        "%R\t\t7\tFront Loaded\tY\n"
        "%R\t\t8\tBell Curve\tN\n"
        "%T\tRSRCCURVDATA\n"
        "%F\tcurv_id\tcurv_name\tdefault_flag\tpct_usage_0\tpct_usage_1\n"
        "%R\t7\tFront Loaded\tY\t100\t90\n"
    )

    def test_parsed(self, tmp_path):
        r = Reader(_xer(tmp_path / "curv.xer", extra_tables=self.CURV_EXTRA))
        curves = list(r.rsrccurves)
        assert len(curves) == 2
        assert curves[0].curv_id == 7
        assert curves[0].curv_name == "Front Loaded"
        assert curves[0].default_flag == "Y"
        assert curves[1].curv_name == "Bell Curve"

    def test_find_by_id(self, tmp_path):
        r = Reader(_xer(tmp_path / "curv.xer", extra_tables=self.CURV_EXTRA))
        assert r.rsrccurves.find_by_id(8).curv_name == "Bell Curve"
        assert r.rsrccurves.find_by_id(999) is None

    def test_no_cross_file_leak(self, tmp_path):
        from xerparser.model.classes.rsrc_curv import RsrcCurv
        Reader(_xer(tmp_path / "curv.xer", extra_tables=self.CURV_EXTRA))
        assert len(RsrcCurv.obj_list) == 2
        # a file without RSRCCURV must not inherit the previous file's curves
        Reader(_xer(tmp_path / "other.xer"))
        assert len(RsrcCurv.obj_list) == 0

    def test_round_trip(self, tmp_path):
        r = Reader(_xer(tmp_path / "curv.xer", extra_tables=self.CURV_EXTRA))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        text = out.read_text()
        assert "%T\tRSRCCURV" in text
        r2 = Reader(out)
        assert r2.rsrccurves.find_by_id(7).curv_name == "Front Loaded"
        assert r2.rsrccurves.find_by_id(8).default_flag == "N"

    def test_absent_not_emitted(self, tmp_path):
        r = Reader(_xer(tmp_path / "one.xer"))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        text = out.read_text()
        assert "%T\tRSRCCURV" not in text
        assert "%T\tRSRCCURVDATA" not in text
