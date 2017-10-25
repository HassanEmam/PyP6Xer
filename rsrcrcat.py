class ResourceCat:
    rsrc_id = ''
    rsrc_catg_type_id = ''
    rsrc_catg_id = ''

    def __init__(self, params):
        self.rsrc_id = params[0].strip()
        self.rsrc_catg_type_id = params[1].strip()
        self.rsrc_catg_id = params[2].strip()


    def get_id(self):
        return self.rsrc_id

    @staticmethod
    def find_by_resource_id(resource_id, resource_cat_dict):
        return {k: v for k, v in resource_cat_dict.items() if v.rsrc_id == resource_id}

    def __repr__(self):
        return self.rsrc_id + ' has been assign category ' + self.rsrc_catg_id
