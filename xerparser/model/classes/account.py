

class Account:
    # obj_list = []

    def __init__(self, params):
        self.acct_id = int(params.get('acct_id').strip()) if params.get('acct_id') else None
        self.parent_acct_id = int(params.get('parent_acct_id').strip()) if params.get('parent_acct_id') else None
        self.acct_seq_num = int(params.get('acct_seq_num').strip()) if params.get('acct_seq_num') else None
        self.acct_name = params.get('acct_name').strip() if params.get('acct_name') else None
        self.acct_short_name = params.get('acct_short_name').strip() if params.get('acct_short_name') else None
        self.acct_descr = params.get('acct_descr').strip() if params.get('acct_descr') else None
        # Account.obj_list.append(self)

    def get_tsv(self):
        tsv = ["%R", self.acct_id, self.parent_acct_id, self.acct_seq_num, self.acct_name, self.acct_short_name,
               self.acct_descr]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.acct_id == id, cls.obj_list))[0]
        return obj

    def __repr__(self):
        return self.acct_name
