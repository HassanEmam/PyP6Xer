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


"""Generic storage for XER tables that have no dedicated model class.

PyP6Xer models the commonly used P6 tables with typed classes. Every other
table in an export (PROJCOST, WBSSTEP, TASKMEMO, ...) used to be silently
dropped on read. ``XerTable``/``XerTables`` preserve those records
losslessly — original headers, column order and row values — and expose
them with dict- and attribute-style access, so a parse followed by a
write round-trips any table the library has no typed model for.
"""

# Column-name suffixes that mark a foreign-key to a type/lookup table
# rather than a row's own identifier (best-effort heuristic).
_FK_SUFFIXES = ('_type_id', '_status_id', '_catg_id', '_catg_type_id')


class XerRecord:
    """One %R row of a generic table.

    Supports attribute access (``record.task_id``), mapping access
    (``record['task_id']``) and ``.get()`` — missing columns yield ``None``
    so older schemas (short rows) never raise.
    """

    def __init__(self, table, headers, values):
        self._table = table
        self._data = dict(zip(headers, values))
        self._raw = list(values)
        self._headers = list(headers)

    def __getattr__(self, name):
        try:
            return self.__dict__['_data'][name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, name):
        return self._data[name]

    def __contains__(self, name):
        return name in self._data

    def __repr__(self):
        return f"<XerRecord {self._table} {self._data!r}>"

    def get(self, name, default=None):
        return self._data.get(name, default)

    def keys(self):
        return list(self._data)

    def to_dict(self):
        return dict(self._data)


class XerTable:
    """All records of one non-modeled XER table, in file order.

    Handles files where the same table appears in several blocks with
    different header sets (each block is preserved separately).
    """

    def __init__(self, name):
        self.name = name
        self._blocks = []  # list of (headers, [raw row lists])

    def add_block(self, headers, rows):
        for existing_headers, existing_rows in self._blocks:
            if list(existing_headers) == list(headers):
                existing_rows.extend(rows)
                return
        self._blocks.append((list(headers), [list(r) for r in rows]))

    def add(self, headers, values):
        self.add_block(headers, [values])

    @property
    def headers(self):
        return list(self._blocks[0][0]) if self._blocks else []

    @property
    def records(self):
        out = []
        for headers, rows in self._blocks:
            out.extend(XerRecord(self.name, headers, r) for r in rows)
        return out

    @property
    def raw_rows(self):
        return [list(r) for _, rows in self._blocks for r in rows]

    def __len__(self):
        return sum(len(rows) for _, rows in self._blocks)

    def __getitem__(self, index):
        return self.records[index]

    def __iter__(self):
        return iter(self.records)

    def _id_column(self, headers):
        candidates = [h for h in headers if isinstance(h, str) and h.endswith('_id')]
        if not candidates:
            return None
        stripped = self.name.lower().replace('_', '')
        exact = [h for h in candidates if h.replace('_', '') == stripped + 'id']
        if exact:
            return exact[0]
        own = [h for h in candidates if not h.endswith(_FK_SUFFIXES)]
        pool = own or candidates
        # Own ids are conventionally the first remaining column; prefer the
        # shortest name as a tiebreak (memo_id over memo_type_id).
        return min(pool, key=len)

    def find_by_id(self, id):
        """Best-effort lookup by the table's own id column.

        Uses the header that matches the table name when present
        (e.g. ``wbs_step_id`` for WBSSTEP), otherwise the most plausible
        non-foreign-key ``*_id`` column. Returns None when the table has
        no usable id column (e.g. TASKFDBK) or no record matches.
        """
        for headers, rows in self._blocks:
            col = self._id_column(headers)
            if col is None:
                continue
            idx = list(headers).index(col)
            for row in rows:
                if idx < len(row) and row[idx] is not None and str(row[idx]) == str(id):
                    return XerRecord(self.name, headers, row)
        return None

    def get_tsv(self):
        """Re-emit this table exactly as parsed (%T/%F/%R blocks, in order)."""
        tsv = []
        for headers, rows in self._blocks:
            tsv.append(['%T', self.name])
            tsv.append(['%F'] + list(headers))
            for row in rows:
                tsv.append(['%R'] + list(row))
        return tsv


class XerTables:
    """Container for every non-modeled table in a file, in first-seen order."""

    def __init__(self):
        self._tables = {}  # name -> XerTable, insertion ordered

    def add(self, table_name, headers, values):
        table = self._tables.get(table_name)
        if table is None:
            table = self._tables[table_name] = XerTable(table_name)
        table.add(headers, values)

    def get(self, table_name):
        return self._tables.get(table_name)

    def __getitem__(self, table_name):
        return self._tables[table_name]

    def __contains__(self, table_name):
        return table_name in self._tables

    def __iter__(self):
        return iter(self._tables.values())

    def __len__(self):
        return len(self._tables)

    @property
    def table_names(self):
        return list(self._tables)
