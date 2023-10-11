import click
import json
import os
import time

from json.decoder import JSONDecodeError
from pathlib import Path
from rich.progress import Progress, BarColumn, TaskID, TextColumn


progress = Progress(
    TextColumn("[bold blue]{task.fields[goal_name]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.completed}%",
    "Completed",
)


def add_goal(goal_name: str, goal_file):
    """Add new goals to the goals.json file. Create a new goals.json file if it doesn't already"""

    if goal_file.exists():
        if os.stat(goal_file).st_size == 0:
            with goal_file.open("w") as f:
                content={goal_name: 0}
                json.dump(content,f)
                print(f"Added goal '{goal_name}' to goals file.\n")
        else:
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
        print("Creating a new goal file to record your goals.\n")
        goal = {goal_name: 0}
        with goal_file.open("w") as f:
            json.dump(goal, f)
        print(f"Added goal '{goal_name}' to the goals file.")

# All other funcs take "goal" as a str but this takes a dict. Need to change.
def update_progress(goal: dict, goal_file):
    """Update goal progress by one step."""

    if goal_file.exists():
        if os.stat(goal_file).st_size == 0:
            print("The goals file is empty. Add some new goals.\n")
            return
        else:
            with goal_file.open("r") as f:
                content=json.load(f)      
            if goal in content:
                print("Goal present in goals set.\n")
                if content[goal] < 100:
                    content[goal]+=1
                    print(f"Progress updated for goal '{goal}'.\n")
                    check_completed_goal(goal_file, content, goal)
                print(f"Goal {content[goal]}% completed.")
                with goal_file.open("w") as f:
                    json.dump(content, f)
            else:
                print("Goal not present in goals list. To add a new goal type 'add <goal>'")
    else: 
        print("The goal file doesn't exist. Create one by adding new goals.\n")


def delete_goal(goal_name: str, goal_file):
    """Delete a goal from the goals file."""

    if goal_file.exists():
        if os.stat(goal_file).st_size == 0:
            print("The goals file is empty. Add some new goals.\n")
            return
        else:
            with goal_file.open("r") as f:
                content=json.load(f)
            if content.get(goal_name) is not None:
                del content[goal_name]
                with goal_file.open("w") as f:
                    json.dump(content, f)
                print("Goal deleted from goals file.\n")
            else:
                print("Goal doesn't exist in the goals file.\n")
    else:
        print("The goal file doesn't exist. Create one by adding new goals.\n")


def check_completed_goal(goal_file, goal: dict, goal_name):
    if goal[goal_name]==100:
        print(f"Woohoo! You have completed your 100 days '{goal_name}' goal! 🎉\n")
        delete_goal(goal_name, goal_file)
        return


def display_goal_list(goal_file):
    """Display all the goals in the goals file."""

    if goal_file.exists():
        if os.stat(goal_file).st_size == 0:
            print("The goals file is empty. Add some new goals.\n")
        else:
            with goal_file.open("r") as f:
                content = json.load(f)
            print("\nYou have the following ongoing goals:\n")
            with progress:
                for k,v in content.items():
                    task_id = progress.add_task("goal", completed=int(v), total=100, goal_name=k)
    else:
        print("The goal file doesn't exist. Create one by adding new goals.\n")

# Maybe I should abstract away the checking for the existance of the goals file

# def check_goals_file_exist(goal_file) -> bool:
#     if not goal_file.exists():
#         print("There is no goals file. Create one by adding new goals.\n")
#         return False
#     else:
#         return True
    
# def check_goals_file_not_empty(goal_file) -> bool:
#     if os.stat(goal_file).st_size == 0:
#         print("The goals file is empty. Add some new goals.\n")
#         return False
#     else:
#         return True

# CLI
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
    """
    
    goal_file = Path("goals.json")
    
    if action=="add":
        print("Enter a new goal.\n")
        goal=input()
        add_goal(goal, goal_file)

    if action=="update":
        print("Enter the goal to update.\n")
        goal=input()
        update_progress(goal, goal_file)

    if action=="show-goals":
        display_goal_list(goal_file)

    if action=="delete":
        print("Enter the goal to delete.\n")
        goal=input()
        delete_goal(goal, goal_file)


if __name__== "__main__":
    main()