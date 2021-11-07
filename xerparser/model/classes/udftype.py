# PyP6XER
# Copyright (C) 2020, 2021 Hassan Emam <hassan@constology.com>
#
# This file is part of PyP6XER.
#
# PyP6XER library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License v2.1 as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyP6XER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>.


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
        # %F	udf_type_id	table_name	udf_type_name	udf_type_label	logical_data_type
        # super_flag	indicator_expression	summary_indicator_expression	export_flag
        self.udf_type_id = params.get('udf_type_id').strip() if params.get('udf_type_id') else None
        self.table_name = params.get('table_name').strip() if params.get('table_name') else None
        self.udf_type_name = params.get('udf_type_name').strip() if params.get('udf_type_name') else None
        self.udf_type_label = params.get('udf_type_label').strip() if params.get('udf_type_label') else None
        self.logical_data_type = params.get('logical_data_type').strip() if params.get('logical_data_type') else None
        self.super_flag = params.get('super_flag').strip() if params.get('super_flag') else None
        self.indicator_expression = params.get('indicator_expression').strip() if params.get(
            'indicator_expression') else None
        self.summary_indicator_expression = params.get('summary_indicator_expression').strip() if params.get(
            'summary_indicator_expression') else None
        self.export_flag = params.get('export_flag').strip() if params.get('export_flag') else None

    def get_id(self):
        return self.udf_type_id

    def get_tsv(self):
        tsv = ['%R', self.udf_type_id, self.table_name, self.udf_type_name, self.udf_type_label, self.logical_data_type,
               self.super_flag, self.indicator_expression, self.summary_indicator_expression, self.export_flag]
        return tsv

    def __repr__(self):
        return self.udf_type_name
