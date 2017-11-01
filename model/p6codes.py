

class ActivityStatus:

    Complete = "TK_Complete"
    InProgress = "TK_Active"
    NotStarted = "TK_NotStart"


class ActivityType:

    Task = "TT_Task"
    StartMilestone = "TT_Mile"
    FinishMilestone = "TT_FinMile"
    LevelOfEffort = "TT_LOE"
    WBSSummary = "TT_WBS"


class RelationshipType:

    FF = "PR_FF"
    FS = "PR_FS"
    SS = "PR_SS"
    SF = "PR_SF"


class DurationTypes:

    FixedQuantity = "DT_FixedQty"
    FixedDurationAndUnits = "DT_FixedDrtn"
    FixedRate = "DT_FixedRate"
    FixedDuration = "DT_FixedDUR2"
