import re

class Calendar:

    obj_list = []

    def __init__(self, params):

        self.clndr_id = params[0].strip()
        self.default_flag = params[1].strip()
        self.clndr_name = params[2].strip()
        self.proj_id = params[3].strip()
        self.base_clndr_id = params[4].strip()
        self.last_chng_date = params[5].strip()
        self.clndr_type = params[6].strip()
        self.day_hr_cnt = float(params[7]) if params[7] else None
        self.week_hr_cnt = float(params[8]) if params[8] else None
        self.month_hr_cnt = float(params[9]) if params[9] else None
        self.year_hr_cnt = float(params[10]) if params[10] else None
        self.rsrc_private = params[11].strip()
        self.clndr_data = params[12].strip()
        Calendar.obj_list.append(self)
        #self.working_hours = self.calendar_workhours()

    def get_id(self):
        return self.clndr_id

    def calendar_workhours(self):
        raw_data = re.findall("DaysOfWeek(.*?)VIEW", self.clndr_data)[0]
        print(raw_data)
        # returns 1st part  \(\d\|\|\d\(\)(.*?)\x7f\x7f
        # returns 2nd part  \(\d\|\|\d\(\w\|(.*?)\)\x7f
        part1 = re.match('\(\d\|\|\d\(\)(.*?)\x7f\x7f .*', raw_data)
        part2 = re.findall('\(\d\|\|\d\(\w\|(.*?)\)\x7f', raw_data)
        print('p1', part1, part2)
        raw_data = re.split("\)\)\x7f", raw_data)[:7]
        rm = raw_data[0]
        rm = rm[4:]
        raw_data[0] = rm
        count =0
        obj = []
        #print(self.clndr_name, raw_data)
        for d in raw_data:
            p1 = re.search('\(\d\|\|\d\(\)', d)
            if p1:
                p1 = p1.group(0)
            #print(p1)
        return obj
    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.clndr_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.clndr_name + ' : ' + str(self.day_hr_cnt) + '\n' + self.clndr_data