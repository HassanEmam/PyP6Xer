class ResourceCat:
    obj_list = []

    def __init__(self, params):
        self.rsrc_id = params[0].strip()
        self.rsrc_catg_type_id = params[1].strip()
        self.rsrc_catg_id = params[2].strip()
        ResourceCat.obj_list.append(self)

    def get_id(self):
        return self.rsrc_id

    def __repr__(self):
        return self.rsrc_id + ' has been assign category ' + self.rsrc_catg_id
