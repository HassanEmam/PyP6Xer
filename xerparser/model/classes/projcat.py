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


class ProjCat:

    def __init__(self, params):
        # %F	proj_id	proj_catg_type_id	proj_catg_id
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.proj_catg_type_id = params.get('proj_catg_type_id').strip() if params.get('proj_catg_type_id') else None
        self.proj_catg_id = params.get('proj_catg_id').strip() if params.get('proj_catg_id') else None


    def get_id(self):
        return self.proj_id

    def get_tsv(self):
        tsv = ['%R', self.proj_id, self.proj_catg_type_id, self.proj_catg_id]
        return tsv

    def __repr__(self):
        return self.proj_catg_name
