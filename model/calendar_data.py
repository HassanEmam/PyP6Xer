import re
import datetime


class CalendarData:
    working_days = dict()
    exceptions = []

    def __init__(self, text):
        self.text = text
        cal2 = []
        cal = re.findall("\(\d\|\|\D+\(\)", text)
        for c in cal:
            c2 = c.split("||")[1]
            cal2.append(c2.split("()")[0])
        val = re.split("\(\d\|\|\D+\(\)", text.strip())
        # print(cal2)
        x = 0

        self.data = dict()
        i = 0
        for c in range(len(cal2)):
            if c >= 1:
                self.data[cal2[c]] = val[c + 1]

            else:
                self.data[cal2[c]] = ''
        # print(self.data)
        self.exceptions = self.get_exceptions()
        self.working_days = self.get_days()

    def xldate_to_datetime(self, xldate):
        temp = datetime.datetime(1899, 12, 30)
        delta = datetime.timedelta(days=xldate)
        return temp + delta

    def get_exceptions(self):
        if self.data['Exceptions']:
            exceptions = self.data['Exceptions'] if self.data['Exceptions'] else None
            # print("Exceptionssss ",exceptions)
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
        first = re.findall("(.*?)\)\x7f\x7f", self.data['DaysOfWeek'])
        days = dict()
        for x in first:
            second = x.split("()")
            days[second[0].split("||")[1]] = (len(second[1].strip()) > 0)
        self.working_days = days
        return self.working_days