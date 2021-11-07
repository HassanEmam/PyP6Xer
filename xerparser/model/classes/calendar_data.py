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


import re
import datetime


class CalendarData:
    working_days = dict()
    exceptions = []

    def __init__(self, text):
        self.text = text
        cal2 = []
        cal = re.findall("\(\d\|\|\d+\(\)", text)
        for c in cal:
            c2 = c.split("||")[1]
            cal2.append(c2.split("()")[0])
        val = re.split("\(\d\|\|\d+\(\)", text.strip())
        x = 0

        self.data = dict()
        i = 0
        for c in range(len(cal2)):
            if c >= 1:
                self.data[cal2[c]] = val[c + 1]

            else:
                self.data[cal2[c]] = ''
        self.exceptions = self.get_exceptions()
        self.working_days = self.get_days()

    def xldate_to_datetime(self, xldate):
        temp = datetime.datetime(1899, 12, 30)
        delta = datetime.timedelta(days=xldate)
        return temp + delta

    def get_work_pattern(self):
        pattern = r"\(\d\|\|\d\(\)\("
        dayName = {2: "Monday", 3: "Tuesday", 4: "Wednesday", 5: "Thursday", 6: "Friday", 7: "Saturday", 1: "Sunday"}
        tx = self.text.split("(0||VIEW(ShowTotal|Y)())")
        days = re.split(pattern, tx[0])
        dys = re.findall(pattern, self.text)
        lst_dow = []
        for day, d in zip(days[1:], dys):
            dow = int(d.replace("(0||", "").replace(")", "").replace("(", ""))
            starts = re.findall("s\|\d\d\:\d\d", day)
            finishes = re.findall("f\|\d\d\:\d\d", day)

            day_dict = {'DayOfWeek': dayName[dow], 'WorkTimes': [], 'ifc': None}
            for s, f in zip(starts, finishes):
                s_c = datetime.datetime.strptime(s.replace("s|", ""), "%H:%M").time()
                f_c = datetime.datetime.strptime(f.replace("f|", ""), "%H:%M").time()
                day_dict['WorkTimes'].append({"Start": s_c, "Finish": f_c})
            lst_dow.append(day_dict)
        return (lst_dow)

    def get_exceptions(self):
        base_datetime = datetime.datetime(1899, 12, 30)
        excep_dates = re.findall(r"\d{5,}", self.text)
        exceptions = []
        for exc in excep_dates:
            exc = int(exc)
            delta = datetime.timedelta(exc)
            exc_date = base_datetime + delta
            dt = datetime.datetime.fromtimestamp(exc, tz=datetime.timezone.utc)
            exceptions.append(exc_date)
        return exceptions

    def get_days(self):
        if not self.data:
            return
        first = re.findall("\(\d\|\|\d\(\)(.*?)\)\)", self.text)
        days = dict()
        i = 0
        for x in first:
            second = x.split("\x7f\x7f")
            x = x.replace("(", "").replace(")", "").replace(" ", "").strip()
            key = str(i + 1)
            if len(x) > 1:
                days[key] = (len(x) > 0)
            else:
                days[key] = False
            i += 1
        self.working_days = days
        return self.working_days