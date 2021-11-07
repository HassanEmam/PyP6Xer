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

    def get_tsv(self):
        tsv = ["%R", self.udf_type_id, self.fk_id, self.proj_id, self.udf_date, self.udf_number, self.udf_text,
               self.udf_code_id]
        return tsv

    @staticmethod
    def find_by_id(code_id, activity_code_dict):
        return {k: v for k, v in activity_code_dict.items() if v.actv_code_id == code_id}

    def __repr__(self):
        return self.udf_text + '->' + self.udf_code_id