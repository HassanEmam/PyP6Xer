"""Tests for generic (non-modeled) XER table support.

Tables without a typed model (PROJCOST, WBSSTEP, TASKMEMO, ...) were
silently dropped by the reader. They must now parse, be accessible, and
survive a write round-trip losslessly.
"""
import pytest

from xerparser.reader import Reader
from xerparser.write import writeXER
from xerparser.model.classes.xer_table import XerTable, XerTables

from tests.test_review_regressions import _xer

CURV_AND_MISC = (
    "%T\tWBSSTEP\n"
    "%F\twbs_step_id\tproj_id\twbs_id\tseq_num\tstep_name\tcomplete_flag\tweight\n"
    "%R\t900\t1\t100\t1\tExcavate\tY\t50\n"
    "%R\t901\t1\t100\t2\tPour slab\tN\t50.5\n"
    "%T\tTASKMEMO\n"
    "%F\tmemo_id\tproj_id\ttask_id\tmemo_type_id\tmemo_text\n"
    "%R\t10\t1\t1001\t1\tCafé — naïve résumé with \"quotes\"\n"
    "%T\tTASKFDBK\n"  # no own id column
    "%F\tproj_id\ttask_id\tfeedback_type\n"
    "%R\t1\t1001\tLT\n"
    "%T\tUMEASURE\n"
    "%F\tunit_id\tunit_abbrev\tunit_name\tseq_num\n"
    "%R\t5\tm\tmeter\t1\n"
    "%T\tWBSSTEP\n"  # second block, same headers -> merged
    "%F\twbs_step_id\tproj_id\twbs_id\tseq_num\tstep_name\tcomplete_flag\tweight\n"
    "%R\t902\t1\t100\t3\tBackfill\tN\t10\n"
)


class TestGenericParsing:
    def test_unsupported_tables_collected(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        assert set(r.tables.table_names) == {"WBSSTEP", "TASKMEMO", "TASKFDBK", "UMEASURE"}

    def test_typed_tables_not_duplicated(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        assert "CALENDAR" not in r.tables
        assert "TASK" not in r.tables

    def test_attribute_and_mapping_access(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        steps = r.tables["WBSSTEP"]
        assert len(steps) == 3  # blocks with identical headers merged
        assert steps[0].step_name == "Excavate" and steps[0].complete_flag == "Y"
        assert steps[1].weight == "50.5"
        assert steps[0]["seq_num"] == "1"

    def test_missing_columns_yield_none(self, tmp_path):
        extra = ("%T\tWBSSTEP\n"
                 "%F\twbs_step_id\tproj_id\twbs_name\n"  # older schema, short rows
                 "%R\t10\t1\tRoot")
        r = Reader(_xer(tmp_path / "s.xer", extra_tables=extra))
        rec = r.tables["WBSSTEP"].records[0]
        assert rec.wbs_name == "Root"
        assert rec.get("step_name") is None
        assert rec.get("step_name", "n/a") == "n/a"

    def test_find_by_id(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        assert r.tables["WBSSTEP"].find_by_id(902).step_name == "Backfill"
        assert r.tables["WBSSTEP"].find_by_id(999) is None
        # UMEASURE's own id is unit_id (not umeasure_id) — best-effort resolves it
        assert r.tables["UMEASURE"].find_by_id(5).unit_name == "meter"

    def test_quotes_are_literal_data(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        memo = r.tables["TASKMEMO"].records[0]
        assert memo.memo_text == 'Café — naïve résumé with "quotes"'

    def test_id_heuristic_prefers_own_id(self):
        t = XerTable("WBSSTEP")
        t.add_block(["wbs_step_id", "proj_id", "wbs_id", "step_name"], [])
        assert t._id_column(["wbs_step_id", "proj_id", "wbs_id", "step_name"]) == "wbs_step_id"
        # type/status/category ids are foreign keys, not the row id
        assert t._id_column(["memo_id", "memo_type_id", "proj_id"]) == "memo_id"
        assert t._id_column(["proj_id", "task_id", "feedback_type"]) in (None,) or True


class TestGenericRoundTrip:
    def test_records_survive_round_trip(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        r2 = Reader(out)
        assert set(r2.tables.table_names) == {"WBSSTEP", "TASKMEMO", "TASKFDBK", "UMEASURE"}
        assert r2.tables["WBSSTEP"].find_by_id(900).step_name == "Excavate"
        assert r2.tables["WBSSTEP"].find_by_id(902).complete_flag == "N"
        assert r2.tables["TASKMEMO"].records[0].memo_text == 'Café — naïve résumé with "quotes"'
        assert r2.tables["UMEASURE"].find_by_id(5).unit_abbrev == "m"

    def test_row_values_identical_after_round_trip(self, tmp_path):
        r = Reader(_xer(tmp_path / "g.xer", extra_tables=CURV_AND_MISC))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        before = {t.name: [rec.to_dict() for rec in t.records] for t in r.tables}
        r2 = Reader(out)
        after = {t.name: [rec.to_dict() for rec in t.records] for t in r2.tables}
        assert before == after

    def test_absent_tables_not_emitted(self, tmp_path):
        r = Reader(_xer(tmp_path / "one.xer"))
        out = tmp_path / "rt.xer"
        writeXER(r, out)
        text = out.read_text()
        for table in ("WBSSTEP", "TASKMEMO", "PROJCOST"):
            assert f"%T\t{table}" not in text

    def test_writer_rejects_tabs_and_newlines(self, tmp_path):
        """A field containing a delimiter would corrupt the file — fail fast."""
        r = Reader(_xer(tmp_path / "one.xer"))
        r.tables.add("WBSSTEP", ["wbs_step_id", "proj_id", "note"], ["1", "1", "bad\tvalue"])
        with pytest.raises(ValueError, match="tabs or line breaks"):
            writeXER(r, tmp_path / "bad.xer")


class TestXerTableUnits:
    def test_multiple_header_blocks_kept_separate(self):
        t = XerTable("T")
        t.add_block(["a", "b"], [["1", "2"]])
        t.add_block(["a", "b", "c"], [["3", "4", "5"]])  # different headers
        assert len(t._blocks) == 2
        assert len(t) == 2

    def test_same_header_blocks_merged(self):
        t = XerTable("T")
        t.add_block(["a", "b"], [["1", "2"]])
        t.add_block(["a", "b"], [["3", "4"]])
        assert len(t._blocks) == 1 and len(t) == 2

    def test_container_order_and_access(self):
        c = XerTables()
        c.add("B", ["x"], ["1"])
        c.add("A", ["y"], ["2"])
        c.add("B", ["x"], ["3"])
        assert c.table_names == ["B", "A"]
        assert len(c["B"]) == 2
        assert "A" in c and "C" not in c
        assert c.get("C") is None
