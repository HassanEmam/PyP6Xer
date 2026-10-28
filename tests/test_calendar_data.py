"""CalendarData (clndr_data) parsing: work patterns, exceptions, working days."""
import datetime

import pytest

from xerparser.model.classes.calendar_data import CalendarData

# P6 stores work-day blocks as (0||<dow>()(s|HH:MMf|HH:MM...)) with dow 1=Sunday,
# exceptions as 5+ digit Excel serial dates. The VIEW marker usually opens the
# string, so the day blocks live after it.
TEXT = (
    "(0||VIEW(ShowTotal|Y)())"
    "(0||2()(s|08:00f|12:00s|13:00f|17:00))"
    "(0||3()(s|08:00f|17:00))"
    "(0||7()())"
    "45658"
)


@pytest.fixture
def cal():
    return CalendarData(TEXT)


def test_data_dict(cal):
    assert "3" in cal.data
    assert "7" in cal.data


def test_work_pattern_days(cal):
    days = cal.get_work_pattern()
    assert [d["DayOfWeek"] for d in days] == ["Monday", "Tuesday", "Saturday"]


def test_work_pattern_times(cal):
    days = cal.get_work_pattern()
    tuesday = days[0]
    assert tuesday["WorkTimes"] == [
        {"Start": datetime.time(8, 0), "Finish": datetime.time(12, 0)},
        {"Start": datetime.time(13, 0), "Finish": datetime.time(17, 0)},
    ]
    assert days[1]["WorkTimes"] == [
        {"Start": datetime.time(8, 0), "Finish": datetime.time(17, 0)}
    ]
    assert days[2]["WorkTimes"] == []  # non-working day


def test_exceptions_as_dates(cal):
    exc = cal.get_exceptions()
    assert len(exc) == 1
    expected = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=45658)
    assert exc[0] == expected


def test_working_days(cal):
    days = cal.get_days()
    assert days == {"1": True, "2": True, "3": False}


def test_xldate_zero():
    cal = CalendarData("")
    assert cal.xldate_to_datetime(0) == datetime.datetime(1899, 12, 30)


def test_empty_text():
    cal = CalendarData("")
    assert cal.get_exceptions() == []
    assert cal.get_days() is None  # no data parsed
    assert cal.get_work_pattern() == []


def test_instance_not_shared():
    a = CalendarData(TEXT)
    b = CalendarData("")
    # class-level mutable defaults must not leak between instances
    assert b.get_exceptions() == []
    assert a.get_exceptions() != []
