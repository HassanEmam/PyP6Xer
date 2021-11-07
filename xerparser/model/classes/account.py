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


class Account:
    # obj_list = []

    def __init__(self, params):
        self.acct_id = int(params.get('acct_id').strip()) if params.get('acct_id') else None
        self.parent_acct_id = int(params.get('parent_acct_id').strip()) if params.get('parent_acct_id') else None
        self.acct_seq_num = int(params.get('acct_seq_num').strip()) if params.get('acct_seq_num') else None
        self.acct_name = params.get('acct_name').strip() if params.get('acct_name') else None
        self.acct_short_name = params.get('acct_short_name').strip() if params.get('acct_short_name') else None
        self.acct_descr = params.get('acct_descr').strip() if params.get('acct_descr') else None
        # Account.obj_list.append(self)

    def get_tsv(self):
        tsv = ["%R", self.acct_id, self.parent_acct_id, self.acct_seq_num, self.acct_name, self.acct_short_name,
               self.acct_descr]
        return tsv

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.acct_id == id, cls.obj_list))[0]
        return obj

    def __repr__(self):
        return self.acct_name
