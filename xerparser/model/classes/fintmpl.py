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


class FinTmpl:


    def __init__(self, params):

        self.fintmpl_id = params.get('fintmpl_id').strip() if params.get('fintmpl_id') else None
        self.fintmpl_name = params.get('fintmpl_name').strip() if params.get('fintmpl_name') else None
        self.default_flag = params.get('default_flag').strip() if params.get('default_flag') else None

    def get_id(self):
        return self.fintmpl_id

    def get_tsv(self):
        tsv = ["%R", self.fintmpl_id, self.fintmpl_name, self.default_flag]
        return tsv


    def __repr__(self):
        return self.proc_id + '->' + self.task_id