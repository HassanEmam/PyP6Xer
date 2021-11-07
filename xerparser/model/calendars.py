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
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.


from xerparser.model.classes.calendar import Calendar


class Calendars:


    def __init__(self):
        self.index = 0
        self._calendars = []

    def add(self, params):
        self._calendars.append(Calendar(params))

    def get_tsv(self):
        if len(self._calendars) > 0:
            tsv = []
            tsv.append(['%T', 'CALENDAR'])
            tsv.append(
                ['%F', 'clndr_id', 'default_flag', 'clndr_name', 'proj_id',
                   'base_clndr_id', 'last_chng_date', 'clndr_type', 'day_hr_cnt',
                   'week_hr_cnt', 'month_hr_cnt', 'year_hr_cnt', 'rsrc_private',
                   'clndr_data'])
            for cal in self._calendars:
                tsv.append(cal.get_tsv())
            return tsv
        return []

    def find_by_id(self, id) -> Calendar:
        obj = list(filter(lambda x: x.clndr_id == id, self._calendars))
        if len(obj) > 0:
            return obj[0]
        return obj

    def count(self):
        return len(self._calendars)

    def __len__(self):
        return len(self._calendars)

    def __iter__(self):
        return self

    def __next__(self) -> Calendar:
        if self.index >= len(self._calendars):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._calendars[idx]