"""Reader and Writer edge cases: malformed input, header handling, idempotence."""
import sys


import pytest

from xerparser.reader import Reader
from xerparser.write import writeXER as Writer

sys.path.insert(0, "tests")
from table_fixtures import build_xer, table_params  # noqa: E402


def _rows_to_text(tmpdir, tables):
    p = tmpdir / "src.xer"
    build_xer(p, tables)
    return p.read_text(encoding="cp1252")


def _write(tmpdir, text, name="t.xer"):
    p = tmpdir / name
    p.write_text(text, encoding="cp1252")
    return str(p)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        Reader(str(tmp_path / "nope.xer"))


def test_empty_file(tmp_path):
    path = _write(tmp_path, "")
    reader = Reader(path)
    assert reader.get_num_lines(path) == 0


def test_header_only(tmp_path):
    path = _write(tmp_path, "ERMHDR\t19.12\t2026-01-02\tProject\tjdoe\n")
    reader = Reader(path)
    assert reader.xer_header is not None


def test_no_ermhdr(tmp_path):
    # file without ERMHDR: reader should tolerate and parse nothing
    path = _write(tmp_path, "%T\tCALENDAR\n%F\tclndr_id\n%R\t1\n%E\n")
    reader = Reader(path)
    assert len(reader.calendars) == 1  # tables still parse


def test_num_lines_counts_rows(tmp_path):
    text_path = tmp_path / "src.xer"
    build_xer(text_path, {"CALENDAR": [table_params("CALENDAR")],
                          "ROLE": [table_params("ROLE")],
                          "RSRC": [table_params("RSRC")]})
    text = text_path.read_text(encoding="cp1252")
    path = _write(tmp_path, text)
    reader = Reader(path)
    assert reader.get_num_lines(path) == 11  # ERMHDR + 3 tables x3 + %E


def test_unicode_content_roundtrip(tmp_path):
    rows = {"CALENDAR": [table_params("CALENDAR", overrides={"clndr_name": "Kaléndär"})],
            "ROLE": [table_params("ROLE", overrides={"role_name": "Ingénieur — rôle"})]}
    path = _write(tmp_path, _rows_to_text(tmp_path, rows))
    reader = Reader(path)
    assert next(iter(reader.calendars)).clndr_name == "Kaléndär"
    assert next(iter(reader.roles)).role_name == "Ingénieur — rôle"


def test_write_idempotent(tmp_path):
    rows = {"CALENDAR": [table_params("CALENDAR")],
            "PROJECT": [table_params("PROJECT")],
            "TASK": [table_params("TASK")]}
    path = _write(tmp_path, _rows_to_text(tmp_path, rows))
    reader = Reader(path)
    out1 = tmp_path / "out1.xer"
    out2 = tmp_path / "out2.xer"
    Writer(reader, str(out1))
    Writer(reader, str(out2))
    assert out1.read_bytes() == out2.read_bytes()


def test_write_default_header_when_none(tmp_path):
    # reader without xer_header (class attr None) still produces ERMHDR output
    rows = {"CALENDAR": [table_params("CALENDAR")]}
    path = _write(tmp_path, _rows_to_text(tmp_path, rows))
    reader = Reader(path)
    reader.xer_header = None  # force default header
    out = tmp_path / "out.xer"
    Writer(reader, str(out))
    text = out.read_text(encoding="cp1252")
    assert text.startswith("ERMHDR\t8.0") and "%T\tCALENDAR" in text


def test_writer_field_with_tab_raises(tmp_path):
    rows = {"CALENDAR": [table_params("CALENDAR")]}
    path = _write(tmp_path, _rows_to_text(tmp_path, rows))
    reader = Reader(path)
    next(iter(reader.calendars)).clndr_name = "bad\tname"
    out = tmp_path / "out.xer"
    with pytest.raises(ValueError, match="tabs or line breaks"):
        Writer(reader, str(out))


def test_writer_escapes_quotes(tmp_path):
    rows = {"CALENDAR": [table_params("CALENDAR", overrides={"clndr_name": 'say "hi"'})]}
    path = _write(tmp_path, _rows_to_text(tmp_path, rows))
    reader = Reader(path)
    out = tmp_path / "out.xer"
    Writer(reader, str(out))
    reparsed = Reader(str(out))
    assert next(iter(reparsed.calendars)).clndr_name == 'say "hi"'
