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
# along with PyP6XER.  If not, see <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html.


class RsrcCurv:
    """A resource curve definition (RSRCCURV table).

    The percentage usage data for a curve lives in RSRCCURVDATA rows that
    reference the curve by curv_id (see xerparser.model.rsrccurves).
    """

    obj_list = []

    def __init__(self, params):
        # Field order per the Oracle P6 XER data map: curv_data, curv_id,
        # curv_name, default_flag.
        self.curv_data = params.get('curv_data').strip() if params.get('curv_data') else None
        self.curv_id = int(params.get('curv_id')) if params.get('curv_id') else None
        self.curv_name = params.get('curv_name').strip() if params.get('curv_name') else None
        self.default_flag = params.get('default_flag').strip() if params.get('default_flag') else None

        RsrcCurv.obj_list.append(self)

    def get_tsv(self):
        tsv = ['%R', self.curv_data, self.curv_id, self.curv_name, self.default_flag]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.curv_id == id, cls.obj_list))
        if len(obj) > 0:
            return obj[0]
        return None

    def __repr__(self):
        return self.curv_name or ""
