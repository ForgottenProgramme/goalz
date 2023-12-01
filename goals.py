# Add a delete_goal_file function
import click
import json
import os
import time

from json.decoder import JSONDecodeError
from pathlib import Path
from rich.progress import Progress, BarColumn, TaskID, TextColumn
from rich.console import Console
from rich.table import Table

# Customize rich.progress object
progress = Progress(
    TextColumn("[bold blue]{task.fields[goal_name]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.completed}%",
    "Completed",
)

#### Model ####

def check_file_exists(file: Path) -> bool:
    """Checks whether the goals.json file exists or not"""
    if file.exists():
        return True
    else:
        print(f"{file} doesn't exist.\n")
        return False


def check_file_not_empty(goal_file) -> bool:
    """Checks whether the goals.json file is non-empty or not"""
    # if os.stat(goal_file).st_size == 0:
    #     print("Goal file is empty. Type `add <goal>` to add a new goal.\n")
    #     return False
    # else:
    #     return True
    with goal_file.open("r") as f:
            try:
                content=json.load(f)
                if not content:
                    return False
                else:
                    return True
            except JSONDecodeError as e:
                if os.stat(goal_file).st_size == 0:
                    print("The goals file is empty. Type `add <goal>` to add a new goal.\n")
                else:
                    print(f"The following error was encountered while trying to read the goals file: {e}\nIf you're unable to locate the file and fix the error, try deleting this goals file using `delete-file` and creating a new one using `add <goal>`.\n")
                return False


def add_goal(goal_name: str, goal_file: Path):
    """Add new goals to the goals.json file. Create a new goals.json file if it doesn't already"""

    goal_name=goal_name.capitalize()
    if check_file_exists(goal_file):
        if check_file_not_empty(goal_file):
            with goal_file.open("r") as f:
                content=json.load(f)
                if content.get(goal_name) is not None:
                    print(f"Goal '{goal_name}' already present in goal set. Update the goal instead.")
                    return
                else:
                    content[goal_name]=0
                    with goal_file.open("w") as f:
                        json.dump(content,f)
                    print(f"Added goal '{goal_name}' to goals file.\n")
        else:
            with goal_file.open("w") as f:
                content={goal_name: 0}
                json.dump(content,f)
                print(f"Added goal '{goal_name}' to goals file.\n")                                    
    else:
        print("Creating a new goal file to record your goals.\n")
        goal = {goal_name: 0}
        with goal_file.open("w") as f:
            json.dump(goal, f)
        print(f"Added goal '{goal_name}' to the goals file.")
    

def update_progress(goal_name: str, goal_file, completed_file):
    """Update goal progress by one step."""
    
    goal_name=goal_name.capitalize()
    if check_file_exists(goal_file):
        if check_file_not_empty(goal_file):
            with goal_file.open("r") as f:
                content=json.load(f)      
            if content.get(goal_name) is not None:
                if content[goal_name] < 99:
                    content[goal_name]+=1
                    print(f"Progress updated for goal '{goal_name}'.\nGoal {content[goal_name]}% completed.\n")
                else:
                    print(f"Yay! You just completed your 100 days goal: {goal_name}! 🎉\nMoving this goal to completed.json file.\n")
                    move_to_completed(goal_name, completed_file)
                    del content[goal_name]

                with goal_file.open("w") as f:
                    json.dump(content, f)      
            else:
                print("Goal not present in goals list. To add a new goal type 'add <goal>'")
        else:
            print("No active goals. Type `add <goal>` to add a new goal.\n")

def delete_goal(goal_name: str, goal_file):
    """Delete a goal from the goals file."""

    goal_name=goal_name.capitalize()
    if check_file_exists(goal_file):
        if check_file_not_empty(goal_file):
            with goal_file.open("r") as f:
                content=json.load(f)
            if content.get(goal_name) is not None:
                del content[goal_name]
                print(content)
                print("Deleted\n")
                with goal_file.open("w") as f:
                    json.dump(content, f)
                print("Goal deleted from goals file.\n")
            else:
                print("Goal doesn't exist in the goals file.\n")


def delete_goal_file(goal_file):
    """Delete the goals.json file"""
    if check_file_exists(goal_file):
        goal_file.unlink()
        print("Deleted goals file. Create a new goals file by adding a goal.\n")
    else:
        print("Goals file doesn't exist. Nothing to delete.\n")


#### View ####

def display_goal_list(goal_file):
    """Display all the goals in the goals file."""

    if check_file_exists(goal_file):
        if check_file_not_empty(goal_file):
            with goal_file.open("r") as f:
                content = json.load(f)
            print("\nYou have the following ongoing goals:\n")
            with progress:
                for k,v in content.items():
                    task_id = progress.add_task("goal", completed=int(v), total=100, goal_name=k)


# TODO: Add function to move 100% completed goal to completed.json file   
def move_to_completed(goal_name: str, completed_file: Path):
    """Moves completed goals to completed.json"""

    goal_name=goal_name.capitalize()
    if check_file_exists(completed_file):
        with completed_file.open("a") as f:
            f.write(f"\n{goal_name}")
    else:
        with completed_file.open("w") as f:
            completed_file.write_text(goal_name)
            print("You completed your first 100 days goal! A new 'completed goals' file was created to store it.\n")


# TODO: Create a function to show completed goals
def display_completed_goals(completed_file: Path):
    """Display completed goals in a table"""

    if not check_file_exists(completed_file):
        print("You have not completed any goals yet.\n")
        return
    table=Table(title="List of Completed Goals")
    table.add_column("Goal Name", justify="left", no_wrap=True)
    with completed_file.open("r") as f:
        goals=f.readlines()
    for goal in goals:
        table.add_row(goal)

    console=Console()
    console.print(table)


#### CLI/Controller ####

@click.command()
@click.argument('action')

def main(action):
    """
    A CLI tool to create and track your "100 Day" goals.\n
    \n
    Usage:\n
    add: To add a new goal to your goals list, type 'add <goal>'.\n 
    update: To update an existing goal type 'update <goal>'.\n
    delete: To delete a goal type 'delete <goal>'.\n
    show-goals: To display a list of all your goals and their percentage completion.\n
    delete-file: To delete the goal file.\n
    """
    
    goal_file = Path("goals.json")
    completed_file = Path("completed.txt")
    
    if action=="add":
        print("Enter a new goal.\n")
        goal=input()
        add_goal(goal, goal_file)

    if action=="update":
        print("Enter the goal to update.\n")
        goal=input()
        update_progress(goal, goal_file, completed_file)

    if action=="show-goals":
        display_goal_list(goal_file)

    if action=="delete":
        print("Enter the goal to delete.\n")
        goal=input()
        delete_goal(goal, goal_file)
    
    if action=="delete-file":
        delete_goal_file(goal_file)

    if action=="show-completed":
        display_completed_goals(completed_file)



if __name__== "__main__":
    main()