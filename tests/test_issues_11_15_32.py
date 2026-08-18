import csv
import os
import tempfile

from xerparser.model.classes.taskpred import TaskPred
from xerparser.model.predecessors import Predecessors
from xerparser.model.roles import Roles
from xerparser.model.tasks import Tasks
from xerparser.reader import Reader


def test_issue_11_lag_hr_cnt_accepts_decimal_values():
    predecessor = TaskPred({"lag_hr_cnt": "12.5"})

    assert predecessor.lag_hr_cnt == 12.5
    assert isinstance(predecessor.lag_hr_cnt, float)


def test_issue_15_reader_accepts_large_xer_fields():
    field = "x" * 131073
    content = (
        "%T\tACCOUNT\n"
        "%F\tacct_id\tparent_acct_id\tacct_seq_num\tacct_name\tacct_short_name\tacct_descr\n"
        f"%R\t1\t\t\t{field}\t\t\n"
    )
    old_limit = csv.field_size_limit()

    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", suffix=".xer", delete=False
    ) as xer_file:
        xer_file.write(content)
        xer_path = xer_file.name

    try:
        csv.field_size_limit(131072)
        reader = Reader(xer_path)

        assert reader.accounts.count() == 1
        assert reader.accounts.get_tsv()[2][4] == field
    finally:
        csv.field_size_limit(old_limit)
        os.unlink(xer_path)


def test_issue_32_collections_can_be_reiterated_and_nested():
    roles = Roles()
    roles.add({"role_id": "1", "role_name": "Role 1"})
    roles.add({"role_id": "2", "role_name": "Role 2"})

    first = list(roles)
    second = list(roles)
    nested = [(outer.role_id, [inner.role_id for inner in roles]) for outer in roles]

    assert [role.role_id for role in first] == [1, 2]
    assert [role.role_id for role in second] == [1, 2]
    assert nested == [(1, [1, 2]), (2, [1, 2])]


def test_issue_32_representative_collections_can_be_reiterated():
    tasks = Tasks()
    tasks.activities.extend(["task 1", "task 2"])
    predecessors = Predecessors()
    predecessors.relations.extend(["pred 1", "pred 2"])

    assert list(tasks) == list(tasks) == ["task 1", "task 2"]
    assert list(predecessors) == list(predecessors) == ["pred 1", "pred 2"]
