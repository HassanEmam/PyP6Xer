"""Resource hierarchy: parent/child, tree building, lookups, JSON export."""
import json
import sys

import pytest

from xerparser.reader import Reader

sys.path.insert(0, "tests")
from table_fixtures import build_xer, table_params  # noqa: E402


@pytest.fixture(scope="module")
def reader(tmp_path_factory):
    # parent first, then child, then grandchild (tests ordering tolerance)
    tables = {"RSRC": [
        table_params("RSRC", overrides={"rsrc_id": "1", "rsrc_name": "Manager",
                                        "parent_rsrc_id": "", "rsrc_type": "RS"}),
        table_params("RSRC", overrides={"rsrc_id": "2", "rsrc_name": "Engineer",
                                        "parent_rsrc_id": "1", "rsrc_type": "RS"}),
        table_params("RSRC", overrides={"rsrc_id": "3", "rsrc_name": "Welder",
                                        "parent_rsrc_id": "2", "rsrc_type": "RS"}),
        table_params("RSRC", overrides={"rsrc_id": "4", "rsrc_name": "Scaffolding",
                                        "parent_rsrc_id": "", "rsrc_type": "RT"}),
    ]}
    path = tmp_path_factory.mktemp("rsrc") / "r.xer"
    build_xer(path, tables)
    return Reader(str(path))


def test_count_and_iter(reader):
    assert len(reader.resources) == 4
    names = {r.rsrc_name for r in reader.resources}
    assert names == {"Manager", "Engineer", "Welder", "Scaffolding"}


def test_get_resource_by_id(reader):
    assert reader.resources.get_resource_by_id(3).rsrc_name == "Welder"
    assert reader.resources.get_resource_by_id(99) is None


def test_get_parent(reader):
    welder = reader.resources.get_resource_by_id(3)
    assert welder.parent_rsrc_id == 2
    parent = reader.resources.get_parent(3)
    assert parent is not None and parent.rsrc_name == "Engineer"


def test_root_resource_has_no_parent(reader):
    assert reader.resources.get_parent(1) is None


def test_build_tree(reader):
    tree = reader.resources.build_tree()
    # two roots: Manager (RS) and Scaffolding (RT); nodes keyed by rsrc_id
    assert len(tree) == 2
    assert 1 in tree[0]  # root node contains its resource
    assert tree[0][1].rsrc_name == "Manager"
    # Engineer nested under Manager as a 'children' list
    kids = tree[0].get("children", [])
    assert len(kids) == 1
    assert kids[0][2].rsrc_name == "Engineer"


def test_to_json(reader):
    welder = reader.resources.get_resource_by_id(3)
    parsed = json.loads(welder.toJson())
    assert parsed["rsrc_name"] == "Welder"
    assert parsed["rsrc_id"] == 3
