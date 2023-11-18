import pytest
import json
import os
import goals
from pathlib import Path


@pytest.fixture()
def temp_goals_file(tmp_path: Path) -> Path:
    GOAL_FILE = {
    "A": 5,
    "B": 10,
    "C": 15,
    }
    p = tmp_path
    p.mkdir(parents= True, exist_ok=True)
    goal_file = (p / "test_goals.json")
    goal_file.write_text(json.dumps(GOAL_FILE))
    return goal_file


def test_add_goal(temp_goals_file):
    goals.add_goal("D", temp_goals_file)
    with temp_goals_file.open("r") as f:
        content = json.load(f)
    assert content == {
        "A": 5,
        "B": 10,
        "C": 15,
        "D": 0,
    }


def test_update_progress(temp_goals_file):
    goals.update_progress("C", temp_goals_file)
    with temp_goals_file.open("r") as f:
        content = json.load(f)
    assert content == {
        "A": 5,
        "B": 10,
        "C": 16,
    }


def test_delete_goal(temp_goals_file):
    goals.delete_goal("C", temp_goals_file)
    with temp_goals_file.open("r") as f:
        content=json.load(f)
        assert content == {
            "A": 5,
            "B": 10,
        }    


def test_file_exists(temp_goals_file):
    assert goals.check_file_exists(temp_goals_file)


def test_file_not_exists(temp_goals_file):
    temp_goals_file.unlink()
    assert not goals.check_file_exists(temp_goals_file)


def test_file_not_empty(temp_goals_file):
    assert goals.check_file_not_empty(temp_goals_file)


def test_file_empty(temp_goals_file):
    goals.delete_goal("A", temp_goals_file)
    goals.delete_goal("B", temp_goals_file)
    goals.delete_goal("C", temp_goals_file)
    assert not goals.check_file_not_empty(temp_goals_file)

