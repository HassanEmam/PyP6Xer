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


from xerparser.model.classes.rsrc import Resource


class Resources:

    def __init__(self):
        self.index = 0
        self._rsrcs = []

    def add(self, params):
        rsrc = Resource(params)
        self._rsrcs.append(rsrc)

    def get_resource_by_id(self, id) -> Resource:
        rsrc = list(filter(lambda x: x.rsrc_id == id, self._rsrcs))
        if len(rsrc) > 0:
            rsrc = rsrc[0]
        else:
            rsrc = None
        return rsrc

    def get_parent(self, id) -> Resource:
        rsrc = list(filter(lambda x: x.rsrc_id == id, self._rsrcs))
        if len(rsrc) > 0:
            rsrc = rsrc[0]
            parent = Resources.get_resource_by_id(rsrc.parent_rsrc_id)
        else:
            rsrc = None
        return rsrc


    def __iter__(self):
        return self

    def __next__(self) -> Resource:
        if self.index >= len(self._rsrcs):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._rsrcs[idx]

    def _get_list(self):
        resor = []
        for res in self._rsrcs:
            resor.append((res.rsrc_id, res.parent_rsrc_id))
        return resor
    
    def get_tsv(self):
        tsv = []
        if len(self._rsrcs) > 0:
            tsv.append(['%T', 'RSRC'])
            tsv.append(['%F', 'rsrc_id', 'parent_rsrc_id', 'clndr_id',
               'role_id', 'shift_id', 'user_id', 'pobs_id',
               'guid', 'rsrc_seq_num', 'email_addr', 'employee_code',
               'office_phone', 'other_phone', 'rsrc_name', 'rsrc_short_name',
               'rsrc_title_name', 'def_qty_per_hr', 'cost_qty_type', 'ot_factor',
               'active_flag', 'auto_compute_act_flag', 'def_cost_qty_link_flag',
               'ot_flag', 'curr_id', 'unit_id', 'rsrc_type', 'location_id', 'rsrc_notes',
               'load_tasks_flag', 'level_flag', 'last_checksum'])
            for rsr in self._rsrcs:
                tsv.append(rsr.get_tsv())
        return tsv
    
    def build_tree(self):
        # pass 1: create nodes dictionary
        a = self._get_list()
        nodes = {}
        for i in a:
            id, parent_id = i
            nodes[id] = {id: self.get_resource_by_id(id)}
        # a = a[1:]
        # pass 2: create trees and parent-child relations
        forest = []
        for i in a:
            id, parent_id = i
            node = nodes[id]
            # either make the node a new tree or link it to its parent
            if parent_id == None or nodes.get(parent_id) == None:
                # start a new tree in the forest
                forest.append(node)
            else:
                # add new_node as child to parent
                parent = nodes.get(parent_id)

                if not 'children' in parent:
                    # ensure parent has a 'children' field
                    parent['children'] = []
                children = parent['children']
                children.append(node)
        return forest
