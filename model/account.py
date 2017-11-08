

class Account:
    obj_list = []

    def __init__(self, params):
        self.acct_id = params[0]
        self.parent_acct_id= params[1]
        self.acct_seq_num = params[2]
        self.acct_name = params[3]
        self.acct_short_name = params[4]
        self.acct_descr = params[5]
        Account.obj_list.append(self)

    def __repr__(self):
        return self.acct_name
