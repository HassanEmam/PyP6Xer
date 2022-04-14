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
import locale

class ResourceCurve:
    obj_list = []

    def __init__(self, params):        
        self.curv_id = int(params.get('curv_id')) if params.get('curv_id') else None
        self.curv_name = params.get('curv_name').strip() if params.get('curv_id') else None
        self.default_flag = params.get('default_flag') if params.get('default_flag') else None
        self.pct_usage_0 = locale.atof(params.get('pct_usage_0')) if params.get('pct_usage_0') else None
        self.pct_usage_1 = locale.atof(params.get('pct_usage_1')) if params.get('pct_usage_1') else None
        self.pct_usage_2 = locale.atof(params.get('pct_usage_2')) if params.get('pct_usage_2') else None
        self.pct_usage_3 = locale.atof(params.get('pct_usage_3')) if params.get('pct_usage_3') else None
        self.pct_usage_4 = locale.atof(params.get('pct_usage_4')) if params.get('pct_usage_4') else None
        self.pct_usage_5 = locale.atof(params.get('pct_usage_5')) if params.get('pct_usage_5') else None
        self.pct_usage_6 = locale.atof(params.get('pct_usage_6')) if params.get('pct_usage_6') else None
        self.pct_usage_7 = locale.atof(params.get('pct_usage_7')) if params.get('pct_usage_7') else None
        self.pct_usage_8 = locale.atof(params.get('pct_usage_8')) if params.get('pct_usage_8') else None
        self.pct_usage_9 = locale.atof(params.get('pct_usage_9')) if params.get('pct_usage_9') else None
        self.pct_usage_10 = locale.atof(params.get('pct_usage_10')) if params.get('pct_usage_10') else None
        self.pct_usage_11 = locale.atof(params.get('pct_usage_11')) if params.get('pct_usage_11') else None
        self.pct_usage_12 = locale.atof(params.get('pct_usage_12')) if params.get('pct_usage_12') else None
        self.pct_usage_13 = locale.atof(params.get('pct_usage_13')) if params.get('pct_usage_13') else None
        self.pct_usage_14 = locale.atof(params.get('pct_usage_14')) if params.get('pct_usage_14') else None
        self.pct_usage_15 = locale.atof(params.get('pct_usage_15')) if params.get('pct_usage_15') else None
        self.pct_usage_16 = locale.atof(params.get('pct_usage_16')) if params.get('pct_usage_16') else None
        self.pct_usage_17 = locale.atof(params.get('pct_usage_17')) if params.get('pct_usage_17') else None
        self.pct_usage_18 = locale.atof(params.get('pct_usage_18')) if params.get('pct_usage_18') else None
        self.pct_usage_19 = locale.atof(params.get('pct_usage_19')) if params.get('pct_usage_19') else None
        self.pct_usage_20 = locale.atof(params.get('pct_usage_20')) if params.get('pct_usage_20') else None

        ResourceCurve.obj_list.append(self)

    def get_tsv(self):
        tsv = ['%R', self.curv_id, self.curv_name, self.default_flag, self.pct_usage_0,
               self.pct_usage_1, self.pct_usage_2, self.pct_usage_3, self.pct_usage_4,
               self.pct_usage_5, self.pct_usage_6, self.pct_usage_7, self.pct_usage_8,
               self.pct_usage_9, self.pct_usage_10, self.pct_usage_11, self.pct_usage_12,
               self.pct_usage_13, self.pct_usage_14, self.pct_usage_15, self.pct_usage_16,
               self.pct_usage_17, self.pct_usage_18, self.pct_usage_19, self.pct_usage_20]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.curv_id == id, cls.obj_list))[0]
        return obj

    def __repr__(self):
        return self.curv_name
