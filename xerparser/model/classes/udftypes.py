

class UDFType:

    udf_type_id = None
    table_name = None
    udf_type_name = None
    udf_type_label = None
    logical_data_type = None
    super_flag = None
    indicator_expression = None
    summary_indicator_expression = None

    def __init__(self, params):

        self.udf_type_id = params[0].strip()
        self.table_name = params[1].strip()
        self.udf_type_name = params[2].strip()
        self.udf_type_label = params[3].strip()
        self.logical_data_type = params[4].strip()
        self.super_flag = params[5].strip()
        self.indicator_expression = params[6].strip()
        self.summary_indicator_expression = params[7].strip()

    def get_id(self):
        return self.udf_type_id

    def __repr__(self):
        return self.udf_type_name
