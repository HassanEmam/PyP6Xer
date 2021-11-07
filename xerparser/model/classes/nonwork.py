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


class NonWork:


    def __init__(self, params):

        self.nonwork_type_id = params.get('nonwork_type_id').strip() if params.get('nonwork_type_id') else None
        self.seq_num = params.get('seq_num').strip() if params.get('seq_num') else None
        self.nonwork_code = params.get('nonwork_code').strip() if params.get('nonwork_code') else None
        self.nonwork_type = params.get('nonwork_type').strip() if params.get('nonwork_type') else None

    def get_id(self):
        return self.nonwork_type_id

    def get_tsv(self):
        tsv = ["%R", self.nonwork_type_id, self.seq_num, self.nonwork_code, self.nonwork_type]
        return tsv


    def __repr__(self):
        return self.nonwork_type_id + '->' + self.nonwork_type