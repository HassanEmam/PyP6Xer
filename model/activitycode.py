class ActivityCode:

    code_list = []

    def __init__(self, params):
        self.actv_code_id = params[0].strip()
        self.parent_actv_code_id = params[1].strip()
        self.actv_code_type_id = params[2].strip()
        self.actv_code_name = params[3].strip()
        self.short_name = params[4].strip()
        self.seq_num = int(params[5]) if params[5] else None
        self.color = params[6].strip()
        self.total_assignments = int(params[7]) if params[7] else None
        ActivityCode.code_list.append(self)

    def get_id(self):
        return self.actv_code_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_id == id, ActivityCode.code_list))
        if obj:
            return obj[0]
        return obj

    @classmethod
    def find_by_code(cls, code):
        """ This Function searches for activity code using ID code

        Args:
            code: ID code as defined in Primavera and not the database
            obj_list: list of activity codes that need to be searched

        Returns: an ActivityCode object that matches the supplied code

        """
        actv_code = list(filter(lambda x: x.short_name == code, ActivityCode.code_list))[0]
        return actv_code

    @classmethod
    def get_parent(cls, id):
        obj = None
        c_actv_code = list(filter(lambda x: x.actv_code_id == id, ActivityCode.code_list))[0]
        if c_actv_code:
            obj = cls.find_by_id(c_actv_code.actv_code_id, ActivityCode.code_list)
        return obj

    @classmethod
    def get_children(cls, id, obj_list):
        childs = list(filter(lambda x: x.parent_actv_code_id == id, obj_list))
        return childs

    def __repr__(self):
        return self.actv_code_id + ' - ' + self.short_name + ' - ' + self.actv_code_name
