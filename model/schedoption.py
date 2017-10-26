
class SchedOption:
    obj_list = []

    def __init__(self, params):

        self.schedoptions_id = params[0].strip()
        self.proj_id = params[1].strip()
        self.sched_outer_depend_type = params[2].strip()
        self.sched_open_critical_flag = params[3].strip()
        self.sched_lag_early_start_flag = params[4].strip()
        self.sched_retained_logic = params[5].strip()
        self.sched_setplantoforecast = params[6].strip()
        self.sched_float_type = params[7].strip()
        self.sched_calendar_on_relationship_lag = params[8].strip()
        self.sched_use_expect_end_flag = params[9].strip()
        self.sched_progress_override = params[10].strip()
        self.level_float_thrs_cnt = params[11].strip()
        self.level_outer_assign_flag = params[12].strip()
        self.level_outer_assign_priority = params[13].strip()
        self.level_over_alloc_pct = params[14].strip()
        self.level_within_float_flag = params[15].strip()
        self.level_keep_sched_date_flag = params[16].strip()
        self.level_all_rsrc_flag = params[17].strip()
        self.sched_use_project_end_date_for_float = params[18].strip()
        self.enable_multiple_longest_path_calc = params[19].strip()
        self.limit_multiple_longest_path_calc = params[20].strip()
        self.max_multiple_longest_path = params[21].strip()
        self.use_total_float_multiple_longest_paths = params[22].strip()
        self.key_activity_for_multiple_longest_paths = params[23].strip()
        self.LevelPriorityList = params[24].strip()
        SchedOption.obj_list.append(self)

    def get_id(self):
        return self.schedoptions_id

    def __repr__(self):
        return self.proj_id