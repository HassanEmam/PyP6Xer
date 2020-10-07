from xerparser.model.tasks import Tasks


class WBS:
    obj_list = []

    def __init__(self, params):
        self.wbs_id = int(params.get('wbs_id').strip()) if params.get('wbs_id') else None
        self.proj_id = int(params.get('proj_id').strip()) if params.get('proj_id') else None
        self.obs_id = params.get('obs_id').strip()
        self.seq_num = params.get('seq_num').strip()
        self.est_wt = params.get('est_wt')
        self.proj_node_flag = params.get('proj_node_flag').strip()
        self.sum_data_flag = params.get('sum_data_flag').strip()
        self.status_code = params.get('status_code').strip()
        self.wbs_short_name = params.get('wbs_short_name').strip()
        self.wbs_name = params.get('wbs_name').strip()
        self.phase_id = params.get('phase_id').strip()
        self.parent_wbs_id = int(params.get('parent_wbs_id')) if params.get('parent_wbs_id') else None
        self.ev_user_pct = params.get('ev_user_pct').strip()
        self.ev_etc_user_value = params.get('ev_etc_user_value').strip()
        self.orig_cost = params.get('orig_cost').strip()
        self.indep_remain_total_cost = params.get('indep_remain_total_cost').strip()
        self.ann_dscnt_rate_pct = params.get('ann_dscnt_rate_pct').strip()
        self.dscnt_period_type = params.get('dscnt_period_type').strip()
        self.indep_remain_work_qty = params.get('indep_remain_work_qty').strip()
        self.anticip_start_date = params.get('anticip_start_date').strip()
        self.anticip_end_date = params.get('anticip_end_date').strip()
        self.ev_compute_type = params.get('ev_compute_type').strip()
        self.ev_etc_compute_type = params.get('ev_etc_compute_type').strip()
        self.guid = params.get('guid').strip()
        self.tmpl_guid = params.get('tmpl_guid').strip()
        self.plan_open_state = params.get('plan_open_state').strip() if params.get('plan_open_state') else None

        WBS.obj_list.append(self)

    def get_id(self):
        return self.wbs_id

    @classmethod
    def get_json(cls):
        root_nodes = list(filter(lambda x: WBS.find_by_id(x.parent_wbs_id) is None, cls.obj_list))
        print(root_nodes)
        json = dict()
        for node in root_nodes:
            json["node"] = node
            json["level"] = 0
            json["childs"] = []
            json["childs"].append(cls.get_childs(node, 0))
        print(json)
        return json

    @classmethod
    def get_childs(cls, node, level):
        nodes_lst = list(filter(lambda x: x.parent_wbs_id == node.wbs_id, cls.obj_list))
        nod = dict()
        for node in nodes_lst:
            nod["node"] = node
            nod["level"] = level + 1
            children = cls.get_childs(node, level + 1)
            nod["childs"] = []
            nod["childs"].append(children)
        return nod
    @classmethod
    def find_by_id(cls, ID):
        obj = list(filter(lambda x: x.wbs_id == ID, cls.obj_list))
        if obj:
            return obj[0]
        return None

    @staticmethod
    def find_by_project_id(project_id, wbs):
        return {k: v for k, v in wbs.items() if v.proj_id == project_id}

    @property
    def activities(self):
        return Tasks.activities_by_wbs_id(self.wbs_id)

    def __repr__(self):
        return self.wbs_name
