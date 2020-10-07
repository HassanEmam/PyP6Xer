

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

        self.udf_type_id = params.get('udf_type_id').strip() if params.get('udf_type_id') else None
        self.table_name = params.get('table_name').strip() if params.get('table_name') else None
        self.udf_type_name = params.get('udf_type_name').strip() if params.get('udf_type_name') else None
        self.udf_type_label = params.get('udf_type_label').strip() if params.get('udf_type_label') else None
        self.logical_data_type = params.get('logical_data_type').strip() if params.get('logical_data_type') else None
        self.super_flag = params.get('super_flag').strip() if params.get('super_flag') else None
        self.indicator_expression = params.get('indicator_expression').strip() if params.get('indicator_expression') else None
        self.summary_indicator_expression = params.get('summary_indicator_expression').strip() if params.get('summary_indicator_expression') else None

    def get_id(self):
        return self.udf_type_id

    def __repr__(self):
        return self.udf_type_name
