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
