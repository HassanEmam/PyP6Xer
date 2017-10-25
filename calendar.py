

class Calendar:

    clndr_id = ''
    default_flag = ''
    clndr_name = ''
    proj_id = ''
    base_clndr_id = ''
    last_chng_date = ''
    clndr_type = ''
    day_hr_cnt = ''
    week_hr_cnt = ''
    month_hr_cnt = ''
    year_hr_cnt = ''
    rsrc_private = ''
    clndr_data = ''

    def __init__(self, params):

        self.clndr_id = params[0].strip()
        self.default_flag = params[1].strip()
        self.clndr_name = params[2].strip()
        self.base_clndr_id = params[3].strip()
        self.last_chng_date = params[4].strip()
        self.clndr_type = params[5].strip()
        self.day_hr_cnt = params[6].strip()
        self.week_hr_cnt = params[7].strip()
        self.month_hr_cnt = params[8].strip()
        self.year_hr_cnt = params[9].strip()
        self.rsrc_private = params[10].strip()
        self.clndr_data = params[11].strip()

    def get_id(self):
        return self.clndr_id

    def __repr__(self):
        return self.clndr_name