

class Account:
    obj_list = []

    def __init__(self, params):
        self.acct_id = int(params[0]) if params[0] else None
        self.parent_acct_id = int(params[1]) if params[1] else None
        self.acct_seq_num = int(params[2]) if params[2] else None
        self.acct_name = params[3]
        self.acct_short_name = params[4]
        self.acct_descr = params[5]
        Account.obj_list.append(self)

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.acct_id == id, cls.obj_list))[0]
        return obj

    def __repr__(self):
        return self.acct_name
