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

    def get_exceptions(self):
        if self.data.get('Exceptions'):
            exceptions = self.data['Exceptions'] if self.data['Exceptions'] else None
            except1 = re.split("\)\)\x7f\x7f", exceptions)
            clean_exceptions = []
            for e in except1:
                if e:
                    if (len(e.split("||"))) > 1:
                        clean_exceptions.append(self.xldate_to_datetime(int(re.findall("\d+", e.split("||")[1])[1])))
                    else:
                        clean_exceptions = None

            self.exceptions = clean_exceptions
        return self.exceptions

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