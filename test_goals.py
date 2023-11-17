import pytest
import json
import goals
from pathlib import Path


GOAL_FILE = {
    "A": 5,
    "B": 10,
    "C": 15,
}

p = Path("temp_path/")
p.mkdir(parents= True, exist_ok=True)
goal_file = (p / "test_goals.json")
goal_file.write_text(json.dumps(GOAL_FILE))

def test_add_goal(goal_file=goal_file):
    goals.add_goal("D", goal_file)
    with goal_file.open("r") as f:
        content = json.load(f)
    assert content == {
        "A": 5,
        "B": 10,
        "C": 15,
        "D": 0,
    }

def test_update_progress(goal_file=goal_file):
    goals.update_progress("D", goal_file)
    with goal_file.open("r") as f:
        content = json.load(f)
    assert content == {
        "A": 5,
        "B": 10,
        "C": 15,
        "D": 1,
    }

def test_delete_goal(goal_file=goal_file):
    goals.delete_goal("C", goal_file)
    with goal_file.open("r") as f:
        content=json.load(f)
        assert content == {
            "A": 5,
            "B": 10,
            "D": 1,
        }    