#!/usr/bin/env python

import json
import os
from datetime import datetime
import rich_click as click

from json.decoder import JSONDecodeError
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from rich.table import Table

#file name constants
GOAL_FILE = Path("goals.json")
COMPLETED_FILE = Path("completed.json")


# Customize rich.progress object
progress = Progress(
    TextColumn("{task.fields[goal_name]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.completed}%",
    "Completed",
)


def check_file_not_empty(file: Path) -> bool:
    """Checks whether a json file is non-empty or not"""

    with file.open("r") as f:
        try:
            content=json.load(f)
            if not content:
                return False
            return True
        except JSONDecodeError as e:
            if os.stat(file).st_size == 0:
                print(f"The {file} file is empty.")
            else:
                print(f"""The following error was encountered while trying to read the file: {e}\nIf you're unable 
                        to locate the file and fix the error, try deleting this file using the `delete-file` command. 
                        You can create a new `{GOAL_FILE}` file by adding a new goal using `add <goal>`, 
                        a new `completed.json` file be created once you complete your first 100 days goal.\n""")
            return False


def add_goal(goal_name: str, file: Path):
    """Add new goals to the {GOAL_FILE} file. Create a new {GOAL_FILE} file if it doesn't already"""

    goal_name=goal_name.capitalize()
    if file.exists():
        if check_file_not_empty(file):
            with file.open("r") as f:
                content=json.load(f)
                if content.get(goal_name) is not None:
                    print(f"Goal '{goal_name}' already present in goal set. Update the goal instead.")
                    return
                else:
                    content[goal_name]=0
                    with file.open("w") as f:
                        json.dump(content,f)
                    print(f"Added goal '{goal_name}' to goals file.\n")
        else:
            with file.open("w") as f:
                content={goal_name: 0}
                json.dump(content,f)
                print(f"Added goal '{goal_name}' to goals file.\n")                                    
    else:
        print("Creating a new goal file to record your goals.\n")
        goal = {goal_name: 0}
        with file.open("w") as f:
            json.dump(goal, f)
        print(f"Added goal '{goal_name}' to the {file} file.")
    

def update_progress(goal_name: str, file: Path):
    """Update goal progress by one step in the {GOAL_FILE} file."""
    
    goal_name=goal_name.capitalize()
    if file.exists():
        if check_file_not_empty(file):
            with file.open("r") as f:
                content=json.load(f)      
            if content.get(goal_name) is not None:
                if content[goal_name] < 99:
                    content[goal_name]+=1
                    print(f"Progress updated for goal '{goal_name}'.\nGoal {content[goal_name]}% completed.\n")
                else:
                    print(f"Yay! You just completed your 100 days goal: {goal_name}! 🎉\nMoving this goal to `completed.json` file.\n")
                    current_date=datetime.now().date().strftime("%-d %b %Y")
                    move_to_completed(goal_name, current_date)
                    del content[goal_name]

                with file.open("w") as f:
                    json.dump(content, f)      
            else:
                print("Goal not present in goals list. Type `add <goal>` to add a new goal.\n")
        else:
            print("No active goals. Type `add <goal>` to add a new goal.\n")


def delete_goal(goal_name: str, file:Path):
    """Delete a goal from the {GOAL_FILE} file."""

    goal_name=goal_name.capitalize()
    if not file.exists():
        print("No active goals. Type `add <goal>` to add a new goal.\n")
        return
    else:
        if not check_file_not_empty(file):
            print("Goal not present in goals list. Type `add <goal>` to add a new goal.\n")
            return 
        else:
            with file.open("r") as f:
                content=json.load(f)
            if content.get(goal_name) is None:
                print("Goal doesn't exist in the goals list.\n")
                return
            else:
                del content[goal_name]
                with file.open("w") as f:
                    json.dump(content, f)
                print("Goal deleted from goals list.\n")
                


def move_to_completed(goal_name: str, date: str):
    """Moves completed goals to completed.json file."""

    goal_name=goal_name.capitalize()

    if not COMPLETED_FILE.exists():
        with COMPLETED_FILE.open("w") as f:
                content= {goal_name: date}
                json.dump(content, f)
        return
    else:
        if not check_file_not_empty(COMPLETED_FILE):
            with COMPLETED_FILE.open("w") as f:
                content= {goal_name: date}
                json.dump(content, f)
            return
        else:
            with COMPLETED_FILE.open("r") as f:
                content=json.load(f)
                content[goal_name]= date
                with COMPLETED_FILE.open("w") as f:
                    json.dump(content, f)
    

@click.group()
def main():
    """
    A CLI tool to track your "100 Day" goals
    """
    pass


@main.command()
@click.argument("goal_name", type=str)
def add(goal_name):
    """
    Add a new goal

    GOAL_NAME: Name of the goal
    """
    add_goal(goal_name, GOAL_FILE)

@main.command()
@click.argument("goal_name", type=str)
def update(goal_name):
    """
    Update the goal progress

    GOAL_NAME: Name of the goal
    """

    update_progress(goal_name)

@main.command()
@click.argument("goal_name", type=str)
def delete(goal_name):
    """
    Delete a goal

    GOAL_NAME: Name of the goal
    """

    delete_goal(goal_name)


@main.command()
def restart():
    """
    Delete everything and start anew
    """

    if GOAL_FILE.exists():
        GOAL_FILE.unlink()
        print("Deleted all ongoing goals.")
    elif COMPLETED_FILE.exists():
        COMPLETED_FILE.unlink()
        print("Deleted all completed goals.")
    else:
        print("Nothing to delete.")


@main.command()
def show_goals():
    """
    Display all current goals
    """

    if not GOAL_FILE.exists():
        print("You have no ongoing goals.\n")
        return
    else:
        if not check_file_not_empty(GOAL_FILE):
            print("The {GOAL_FILE} file is empty. You have no ongoing goals.\n")
            return
        else:
            with GOAL_FILE.open("r") as f:
                content = json.load(f)
            print("\nYou have the following ongoing goals:\n")
            with progress:
                for k,v in content.items():
                    task_id = progress.add_task("goal", completed=int(v), total=100, goal_name=k)        


@main.command()
def show_completed():
    """
    Display all completed goals
    """

    if not COMPLETED_FILE.exists() or not check_file_not_empty(COMPLETED_FILE):
        print("You have not completed any goals yet.\n")
        return
    
    table=Table(title="List of Completed Goals")
    table.add_column("Goal Name", justify="left", no_wrap=True)
    table.add_column("Date Completed", justify="center", no_wrap=True)
    with COMPLETED_FILE.open("r") as f:
        goals=json.load(f)
        for goal in goals:
            table.add_row(goal, goals[goal])

    console=Console()
    console.print(table)


if __name__== "__main__":
    main()