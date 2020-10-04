class UDFValue:

    udf_code_id = None
    udf_type_id = None
    fk_id = None
    proj_id = None
    udf_number = None
    udf_text = None

    def __init__(self, params):

        self.udf_type_id = params[0].strip()
        self.fk_id = params[1].strip()
        self.proj_id = params[2].strip()
        self.udf_date = params[3].strip()
        self.udf_number = params[4].strip()
        self.udf_text = params[5].strip()
        self.udf_code_id = params[6].strip()

    def get_id(self):
        return self.udf_type_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.udf_text + '->' + self.udf_code_id