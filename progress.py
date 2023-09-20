import argparse
import json

from pathlib import Path


HELP_MESSAGE ="To add a new goal to your goals list, type 'add <goal>'.\n To update an existing goal type 'update <goal>'."


def add_goal(goal_name: str, goal_file)-> None:
    with goal_file.open("r") as f:
        content=json.load(f)
    if content[goal_name]:
        print(f"Goal '{goal_name}' already present in goal set. Update the goal instead.")
        return
    else:
        goal = {goal_name: 0}
        with goal_file.open("w") as f:
            json.dump(goal, f)
        print(f"Added goal {goal} to the goals list.")


def update_progress(goal: dict, goal_file):
    with goal_file.open("r") as f:
        content=json.load(f)
        
    if goal in content:
        print("Goal present in goals set.\n")
        if content[goal] < 100:
            content[goal]+=1
            print("Progress updated.\n")
        print(f"Goal {content[goal]}% completed.")
        with goal_file.open("w") as f:
            json.dump(content, f)
    else:
        print("Goal not present in goals list. To add a new goal type 'add <goal>'")


def display_goal_list(goal_file):
    with goal_file.open("r") as f:
        content = json.load(f)
    for k,v in content.items():
        print("You have the following ongoing goals:\n")
        print(f"{k}: {v}%\n")


# CLI
parser = argparse.ArgumentParser(
    prog="100-days-goal",
    description="A CLI application to track your 100-days goal progress.",
    add_help=True,
)

parser.add_argument('action',
    action='store',
    default=None,
    help=f"add: to add a new goal, update: to update an existing goal, show-goals: to show the list of your existing goals.\n"    
    )

args = parser.parse_args()


def main():
    goal_file = Path("goals.json")

    if args.action=="add":
        print("Enter a new goal.\n")
        goal=input()
        add_goal(goal, goal_file)

    if args.action=="update":
        print("Enter the goal to update.\n")
        goal=input()
        update_progress(goal, goal_file)

    if args.action=="show-goals":
        display_goal_list(goal_file)

if __name__== "__main__":
    main()