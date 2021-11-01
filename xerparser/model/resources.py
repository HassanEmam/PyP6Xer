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
