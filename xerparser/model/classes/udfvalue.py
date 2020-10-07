class UDFValue:

    udf_code_id = None
    udf_type_id = None
    fk_id = None
    proj_id = None
    udf_number = None
    udf_text = None

    def __init__(self, params):

        self.udf_type_id = params.get('udf_type_id').strip() if params.get('udf_type_id') else None
        self.fk_id = params.get('fk_id').strip() if params.get('fk_id') else None
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.udf_date = params.get('udf_date').strip() if params.get('udf_date') else None
        self.udf_number = params.get('udf_number').strip() if params.get('udf_number') else None
        self.udf_text = params.get('udf_text').strip() if params.get('udf_text') else None
        self.udf_code_id = params.get('udf_code_id').strip() if params.get('udf_code_id') else None

    def get_id(self):
        return self.udf_type_id

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.udf_text + '->' + self.udf_code_id