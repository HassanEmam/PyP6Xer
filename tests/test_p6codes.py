"""P6 code/enum helper classes."""
from xerparser.model.classes.p6codes import (
    ActivityStatus,
    ActivityType,
    DurationTypes,
    RelationshipType,
)


def test_activity_status():
    assert ActivityStatus.Complete == "TK_Complete"
    assert ActivityStatus.InProgress == "TK_Active"
    assert ActivityStatus.NotStarted == "TK_NotStart"


def test_activity_type():
    assert ActivityType.Task == "TT_Task"
    assert ActivityType.StartMilestone == "TT_Mile"
    assert ActivityType.FinishMilestone == "TT_FinMile"
    assert ActivityType.LevelOfEffort == "TT_LOE"
    assert ActivityType.WBSSummary == "TT_WBS"


def test_relationship_type():
    assert RelationshipType.FS == "PR_FS"
    assert RelationshipType.SS == "PR_SS"
    assert RelationshipType.FF == "PR_FF"
    assert RelationshipType.SF == "PR_SF"


def test_duration_types():
    assert DurationTypes.FixedQuantity == "DT_FixedQty"
    assert DurationTypes.FixedDurationAndUnits == "DT_FixedDrtn"
    assert DurationTypes.FixedRate == "DT_FixedRate"
