import time
import json

from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
)
from pathlib import Path

goal_file = Path("goals.json")

progress = Progress(
    TextColumn("[bold blue]somethign", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]%",
    "•",
)


with progress:
    # with goal_file.open("r") as f:
    #     content=json.load(f)
    #     for k,v in content.items():


    task1 = progress.add_task("[red]Downloading...", total=100)
    task2 = progress.add_task("[green]Processing...", total=100)
    task3 = progress.add_task("[cyan]Cooking...", total=100)

    while not progress.finished:
        progress.update(task1, advance=1)
        progress.update(task2, advance=1)
        progress.update(task3, advance=1)
        time.sleep(0.02)