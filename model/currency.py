

class Currency:
    obj_list = []

    def __init__(self, params):

        self.curr_id = params[0].strip()
        self.decimal_digit_cnt = params[1].strip()
        self.curr_symbol = params[2].strip()
        self.decimal_symbol = params[3].strip()
        self.digit_group_symbol = params[4].strip()
        self.pos_curr_fmt_type = params[5].strip()
        self.neg_curr_fmt_type = params[6].strip()
        self.curr_type = params[7].strip()
        self.curr_short_name = params[8].strip()
        self.group_digit_cnt = params[9].strip()
        self.base_exch_rate = params[10].strip()
        Currency.obj_list.append(self)

    def get_id(self):
        return self.curr_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.curr_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.curr_symbol + ' ' + self.curr_type