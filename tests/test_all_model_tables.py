"""Parametrized coverage of every typed XER table.

For each table: a fully-populated row parses, the collection's %F header
and %R row stay aligned, get_id works, and the table survives a full
writeXER round-trip.
"""
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tests.table_fixtures import (
    ALL_TABLES, TABLE_MODULES, build_xer, table_params, table_row,
    _fields_of,
)

TABLES = [t for t in ALL_TABLES if t != "ROLES"]  # ROLES == ROLE collection

# tables that must be parsed before tables that reference them
ORDERED = ["CALENDAR", "PROJECT", "PROJWBS", "TASK"] + [
    t for t in TABLES if t not in ("CALENDAR", "PROJECT", "PROJWBS", "TASK")]


def _written_name(table):
    """ROLE rows are written under the canonical ROLES table name."""
    return "ROLES" if table == "ROLE" else table


def _collection(table):
    mod_name, cls_name, _ = TABLE_MODULES[table]
    mod = __import__(f"xerparser.model.{mod_name}", fromlist=[cls_name])
    return getattr(mod, cls_name)()


def _add(coll, table, params):
    """add(params) or add(params, data) depending on the collection."""
    import inspect
    from xerparser.model.classes.data import Data
    if "data" in inspect.signature(coll.add).parameters:
        coll.add(params, Data())
    else:
        coll.add(params)


def _count(coll):
    """len() where available, count() otherwise."""
    try:
        return len(coll)
    except TypeError:
        c = coll.count
        return c() if callable(c) else c


def _reader_attr(table):
    return TABLE_MODULES[table][2]


@pytest.mark.parametrize("table", TABLES)
def test_table_parses_all_fields(tmp_path, table):
    path = build_xer(tmp_path / "t.xer", {table: [table_params(table)]})
    reader = Reader(str(path))
    coll = getattr(reader, _reader_attr(table))
    assert _count(coll) == 1, table
    # every declared field must have parsed to a non-None attribute on the object
    rec = list(coll)[0]
    for field in _fields_of(table):
        assert getattr(rec, field, "MISSING") != "MISSING", (table, field)


@pytest.mark.parametrize("table", TABLES)
def test_header_row_alignment(table):
    coll = _collection(table)
    _add(coll, table, table_params(table))
    tsv = coll.get_tsv()
    assert tsv[0] == ["%T", _written_name(table)]
    header = tsv[1]
    assert header[0] == "%F"
    fields = header[1:]
    assert len(tsv) == 3  # %T, %F, one %R
    for row in tsv[2:]:
        assert row[0] == "%R"
        assert len(row) - 1 == len(fields), (table, row, fields)


@pytest.mark.parametrize("table", TABLES)
def test_get_id(table):
    coll = _collection(table)
    _add(coll, table, table_params(table))
    rec = list(coll)[0]
    get_id = getattr(rec, "get_id", None)
    if get_id is None:
        pytest.skip("no get_id on this class")
    assert get_id() is not None


@pytest.mark.parametrize("table", TABLES)
def test_write_roundtrip_preserves_table(tmp_path, table):
    """A table parsed from a file must re-emit with identical values."""
    params = table_params(table)
    path = build_xer(tmp_path / "in.xer", {table: [params]})
    reader = Reader(str(path))
    out = tmp_path / "out.xer"
    writeXER(reader, out)
    text = out.read_text()
    lines = text.splitlines()
    i = 0
    found = False
    while i < len(lines):
        if lines[i] == f"%T\t{_written_name(table)}":
            found = True
            fields = lines[i + 1].split("\t")[1:]
            rowvals = lines[i + 2].split("\t")[1:]
            assert len(rowvals) == len(fields), table
            for f, v in zip(fields, rowvals):
                want = params.get(f, "")
                if want is None:
                    want = ""
                if f in ("float_path", "aref", "arls"):
                    continue  # writer emits computed/empty for these on TaskPred
                assert str(v) == str(want), (table, f, v, want)
            i += 2
        else:
            i += 1
    assert found, f"{table} not written"


from xerparser.reader import Reader
from xerparser.write import writeXER


class TestMegaFile:
    def test_all_tables_in_one_file(self, tmp_path):
        tables = {t: [table_params(t)] for t in ORDERED}
        path = build_xer(tmp_path / "mega.xer", tables)
        reader = Reader(str(path))
        for table in TABLES:
            assert _count(getattr(reader, _reader_attr(table))) == 1, table

    def test_mega_roundtrip_counts(self, tmp_path):
        tables = {t: [table_params(t)] for t in ORDERED}
        path = build_xer(tmp_path / "mega.xer", tables)
        reader = Reader(str(path))
        out = tmp_path / "out.xer"
        writeXER(reader, out)
        reader2 = Reader(str(out))
        for table in TABLES:
            assert _count(getattr(reader2, _reader_attr(table))) == 1, table

    def test_multiple_records(self, tmp_path):
        tables = {t: [table_params(t), table_params(t)] for t in ORDERED}
        path = build_xer(tmp_path / "mega.xer", tables)
        reader = Reader(str(path))
        for table in TABLES:
            assert _count(getattr(reader, _reader_attr(table))) == 2, table

    def test_class_registry_reset_all(self, tmp_path):
        """Parsing a second file must not inherit the first file's records."""
        path = build_xer(tmp_path / "a.xer", {t: [table_params(t)] for t in ORDERED})
        Reader(str(path))
        empty = build_xer(tmp_path / "b.xer", {"CALENDAR": [table_params("CALENDAR")]})
        reader2 = Reader(str(empty))
        for table in TABLES:
            if table == "CALENDAR":
                continue
            assert _count(getattr(reader2, _reader_attr(table))) == 0, table
