"""Shared fixtures: build spec-valid XER tables for every typed model.

Field types (int/float/date) are derived from each model class's own
__init__ source, so generated rows always parse.
"""
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

# table name -> collection module (relative to xerparser/model/)
TABLE_MODULES = {
    "ACCOUNT": ("accounts", "Accounts", "_accounts"),
    "ACTVCODE": ("activitycodes", "ActivityCodes", "_actvcodes"),
    "ACTVTYPE": ("acttypes", "ActTypes", "_acttypes"),
    "CALENDAR": ("calendars", "Calendars", "_calendars"),
    "CURRTYPE": ("currencies", "Currencies", "_currencies"),
    "FINTMPL": ("fintmpls", "FinTmpls", "_fintmpls"),
    "NONWORK": ("nonworks", "NonWorks", "_nonworks"),
    "OBS": ("obss", "OBSs", "_obss"),
    "PCATTYPE": ("pacttypes", "PCatTypes", "_pcattypes"),
    "PCATVAL": ("pcatvals", "PCatVals", "_pcatvals"),
    "PROJPCAT": ("projcats", "ProjCats", "_projpcats"),
    "PROJECT": ("projects", "Projects", "_projects"),
    "RCATTYPE": ("rcattypes", "RCatTypes", "_rcattypes"),
    "RCATVAL": ("rcatvals", "RCatVals", "_rcatvals"),
    "ROLE": ("roles", "Roles", "_roles"),
    "ROLES": ("roles", "Roles", "_roles"),
    "ROLERATE": ("rolerates", "RoleRates", "_rolerates"),
    "RSRC": ("resources", "Resources", "_resources"),
    "RSRCCURV": ("rsrc_curvs", "RsrcCurves", "_rsrc_curvs"),
    "RSRCCURVDATA": ("rsrccurves", "ResourceCurves", "_rsrcurves"),
    "RSRCRATE": ("rsrcrates", "ResourceRates", "_rsrcrates"),
    "RSRCRCAT": ("rsrccats", "ResourceCategories", "_rsrccats"),
    "SCHEDOPTIONS": ("schedoptions", "SchedOptions", "_schedoptions"),
    "TASK": ("tasks", "Tasks", "_tasks"),
    "TASKACTV": ("taskactvs", "TaskActvs", "_activitycodes"),
    "TASKPRED": ("predecessors", "Predecessors", "_predecessors"),
    "TASKPROC": ("taskprocs", "TaskProcs", "_taskprocs"),
    "TASKRSRC": ("activitiyresources", "ActivityResources", "_activityresources"),
    "UDFTYPE": ("udftypes", "UDFTypes", "_udftypes"),
    "UDFVALUE": ("udfvalues", "UDFValues", "_udfvalues"),
    "PROJWBS": ("wbss", "WBSs", "_wbss"),
}

# table -> model class source file in xerparser/model/classes/
TABLE_CLASS_FILES = {
    "ACCOUNT": "account.py", "ACTVCODE": "activitycode.py", "ACTVTYPE": "acttype.py",
    "CALENDAR": "calendar.py", "CURRTYPE": "currency.py", "FINTMPL": "fintmpl.py",
    "NONWORK": "nonwork.py", "OBS": "obs.py", "PCATTYPE": "pcattype.py",
    "PCATVAL": "pcatval.py", "PROJPCAT": "projcat.py", "PROJECT": "project.py",
    "RCATTYPE": "rcattype.py", "RCATVAL": "rcatval.py", "ROLE": "role.py",
    "ROLES": "role.py", "ROLERATE": "rolerate.py", "RSRC": "rsrc.py",
    "RSRCCURV": "rsrc_curv.py", "RSRCCURVDATA": "rsrccurv.py", "RSRCRATE": "rsrcrate.py",
    "RSRCRCAT": "rsrcrcat.py", "SCHEDOPTIONS": "schedoption.py", "TASK": "task.py",
    "TASKACTV": "taskactv.py", "TASKPRED": "taskpred.py", "TASKPROC": "taskproc.py",
    "TASKRSRC": "taskrsrc.py", "UDFTYPE": "udftype.py", "UDFVALUE": "udfvalue.py",
    "PROJWBS": "wbs.py",
}

INT_FIELDS = {}      # table -> set of fields parsed with int()
FLOAT_FIELDS = {}    # table -> set of fields parsed with float()
DATE_FIELDS = {}     # table -> set of datetime-parsed fields
TABLE_FIELDS = {}    # table -> ordered field list from the collection %F header


def _class_source(table):
    return (REPO / "xerparser" / "model" / "classes" / TABLE_CLASS_FILES[table]).read_text()


def _fields_of(table):
    """The collection's %F field list (single- or double-quoted source)."""
    if table in TABLE_FIELDS:
        return TABLE_FIELDS[table]
    sources = [_class_source(table),
               (REPO / "xerparser" / "model" / f"{TABLE_MODULES[table][0]}.py").read_text()]
    for src in sources:
        m = re.search(r"['\"]%F['\"]([^\]]*)\]", src)
        if m:
            fields = re.findall(r"['\"]([^'\"]+)['\"]", m.group(1))
            fields = [f for f in fields if f != "%F"]
            TABLE_FIELDS[table] = fields
            return fields
    raise ValueError(f"no %F header found for {table}")


def _parsed_types(table):
    """Extract int/float/date field sets from the model class source."""
    if table in INT_FIELDS:
        return
    src = _class_source(table)
    ints = set(re.findall(r"int\(params\.get\('(\w+)'\)", src))
    ints |= set(re.findall(r"int\(float\(params\.get\('(\w+)'\)(?:\.strip\(\))?\)\)", src))
    floats = set(re.findall(r"float\(params\.get\('(\w+)'\)", src))
    dates = set(re.findall(r"(?:strptime|fromisoformat)\(params\.get\('(\w+)'\)", src))
    INT_FIELDS[table] = ints
    FLOAT_FIELDS[table] = floats
    DATE_FIELDS[table] = dates


def field_value(table, field):
    """A parseable, round-trip-stable value for one field."""
    _parsed_types(table)
    if field in INT_FIELDS[table]:
        return "7"
    if field in DATE_FIELDS[table]:
        return "2026-01-05 08:00"
    if field in FLOAT_FIELDS[table]:
        return "2.5"
    if field.endswith("_flag"):
        return "Y"
    if field.endswith("_id"):
        return "42"
    if field == "pred_type":
        return "PR_FS"
    if field == "clndr_type":
        return "CA_Calendar"
    if field == "status_code":
        return "TK_NotStart"
    return f"S_{field[:24]}"


def table_params(table, overrides=None):
    """A params dict for the table's model class, keyed by real header."""
    fields = _fields_of(table)
    params = {f: field_value(table, f) for f in fields}
    if overrides:
        params.update(overrides)
    return params


def table_row(table, overrides=None):
    params = table_params(table, overrides)
    fields = _fields_of(table)
    return [params.get(f, "") for f in fields]


def build_xer(path, tables=None, header=("19.12", "2026-01-02", "Project", "jdoe")):
    """Write an XER containing the given tables (name -> list of param dicts)."""
    rows = ["ERMHDR\t" + "\t".join(header)]
    for table, records in (tables or {}).items():
        fields = _fields_of(table)
        rows.append("%T\t" + table)
        rows.append("%F\t" + "\t".join(fields))
        for rec in records:
            rows.append("%R\t" + "\t".join(str(rec.get(f, "")) for f in fields))
    rows.append("%E")
    path.write_text("\n".join(rows) + "\n", encoding="cp1252")
    return path


ALL_TABLES = sorted(TABLE_MODULES)


@pytest.fixture(scope="session")
def all_tables_params():
    """table -> list with a single fully-populated params dict."""
    return {t: [table_params(t)] for t in ALL_TABLES}
