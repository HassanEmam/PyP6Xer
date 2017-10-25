

class Currency:
    curr_id = ''
    decimal_digit_cnt = '' 
    curr_symbol = '' 
    decimal_symbol = ''
    digit_group_symbol = ''
    pos_curr_fmt_type = ''
    neg_curr_fmt_type = ''
    curr_type = ''
    curr_short_name = ''
    group_digit_cnt = ''
    base_exch_rate = ''

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

    def get_id(self):
        return self.curr_id

    def __repr__(self):
        return self.curr_symbol + ' ' + self.curr_type