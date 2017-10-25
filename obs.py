

class OBS:
    obs_id = ''
    parent_obs_id = ''
    guid = ''
    seq_num = ''
    obs_name = ''
    obs_descr = ''

    def __init__(self, params):
        self.obs_id = params[0].strip()
        self.parent_obs_id = params[1].strip()
        self.guid = params[2].strip()
        self.seq_num = params[3].strip()
        self.obs_name = params[4].strip()
        self.obs_descr = params[5].strip()

    def get_id(self):
        return self.obs_id

    def __repr__(self):
        return self.obs_name
