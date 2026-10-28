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
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html.


def _default_header():
    return ['ERMHDR', '8.0', '2021-11-02', 'Project', 'admin', 'Primavera', 'Admin', 'dbxDatabaseNoName', 'Project Management', 'U.K.']


def _field(value):
    """Format one XER field.

    XER is tab-separated with NO quoting: quote characters are literal
    data, so rows are joined directly. (csv.writer, even with
    QUOTE_NONE, doubled or rejected quote characters.) Tabs and line
    breaks cannot appear in a field without corrupting the file, so we
    fail fast instead of silently writing an ambiguous row.
    """
    if value is None:
        return ''
    s = str(value)
    if '\t' in s or '\n' in s or '\r' in s:
        raise ValueError(
            f"XER fields cannot contain tabs or line breaks: {s[:80]!r}")
    return s


def _write_rows(output, rows):
    for row in rows:
        output.write('\t'.join(_field(v) for v in row) + '\r\n')


def writeXER(r, filename):
    # Preserve the ERMHDR from the source file when the Reader was parsed
    # from a file, so a round-trip does not fake version/user/database info.
    header = None
    if hasattr(r, 'xer_header') and isinstance(r.xer_header, list) and r.xer_header and r.xer_header[0] == 'ERMHDR':
        header = list(r.xer_header)
    if not header:
        header = _default_header()
    with open(filename, 'w', newline='', encoding='utf-8') as output:
        _write_rows(output, [header])
        _write_rows(output, r.currencies.get_tsv())
        _write_rows(output, r.fintmpls.get_tsv())
        _write_rows(output, r.nonworks.get_tsv())
        _write_rows(output, r.obss.get_tsv())
        _write_rows(output, r.pcattypes.get_tsv())
        _write_rows(output, r.rsrccurves.get_tsv())  # RSRCCURV (definitions)
        _write_rows(output, r.resourcecurves.get_tsv())  # RSRCCURVDATA
        _write_rows(output, r.udftypes.get_tsv())
        _write_rows(output, r.accounts.get_tsv())
        _write_rows(output, r.pcatvals.get_tsv())
        _write_rows(output, r.projects.get_tsv())
        _write_rows(output, r.calendars.get_tsv())
        _write_rows(output, r.projpcats.get_tsv())
        _write_rows(output, r.roles.get_tsv())
        _write_rows(output, r.rolerates.get_tsv())
        _write_rows(output, r.rcattypes.get_tsv())
        _write_rows(output, r.rcatvals.get_tsv())
        _write_rows(output, r.resourcecategories.get_tsv())
        # Only write SCHEDOPTIONS if it exists and has data
        try:
            if hasattr(r, 'scheduleoptions') and r.scheduleoptions and len(r.scheduleoptions) > 0:
                _write_rows(output, r.scheduleoptions.get_tsv())
        except (AttributeError, TypeError):
            # Skip SCHEDOPTIONS if not present or cannot be accessed
            pass
        _write_rows(output, r.wbss.get_tsv())
        _write_rows(output, r.resources.get_tsv())
        _write_rows(output, r.acttypes.get_tsv())
        _write_rows(output, r.resourcerates.get_tsv())
        _write_rows(output, r.activities.get_tsv())
        _write_rows(output, r.actvcodes.get_tsv())
        _write_rows(output, r.relations.get_tsv())
        _write_rows(output, r.taskprocs.get_tsv())
        _write_rows(output, r.activityresources.get_tsv())
        _write_rows(output, r.taskactvs.get_tsv())
        _write_rows(output, r.udfvalues.get_tsv())
        # Generic (non-modeled) tables, in original file order — emitted last
        # so nothing parsed is ever dropped on write.
        xer_tables = getattr(r, 'tables', None)
        if xer_tables is not None:
            for table in xer_tables:
                _write_rows(output, table.get_tsv())
        _write_rows(output, [['%E']])
