

class OBS:
    obj_list = []

    def __init__(self, params):
        self.obs_id = params[0].strip()
        self.parent_obs_id = params[1].strip()
        self.guid = params[2].strip()
        self.seq_num = params[3].strip()
        self.obs_name = params[4].strip()
        self.obs_descr = params[5].strip()
        OBS.obj_list.append(self)

    def get_id(self):
        return self.obs_id

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.obs_id == id, cls.obj_list))
        if obj:
            return obj[0]
        return obj

    def __repr__(self):
        return self.obs_name
