#! .venv/bin/python3.13

from random import randint

from rich import print
from rich.highlighter import Highlighter
from rich.console import Console
from rich.table import Table
from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

import json
from urllib.request import urlopen

from rich.columns import Columns

from datetime import datetime

from rich.align import Align
from rich.layout import Layout
from rich.text import Text


"""

This example demonstrates how to write a custom highlighter.

"""
class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)


rainbow = RainbowHighlighter()
print(rainbow("I must not fear. Fear is the mind-killer."))


"""

Demonstrates how to render a table.

"""
table = Table(title="Star Wars Movies")

table.add_column("Released", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019",
              "Star Wars: The Rise of Skywalker",
              "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017",
              "Star Wars Ep. V111: The Last Jedi",
              "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()

console.print(table, justify="center")


"""
This example shows how to display content in columns.

The data is pulled from https://randomuser.me
"""
def get_content(user):
    """Extract text from user dict."""
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"
    return f"[b]{name}[/b]\n[yellow]{country}"


users = json.loads(
    urlopen("https://randomuser.me/api/?results=30").read()
)["results"]

# console.print(users, overflow="ignore", crop=False)
user_renderables = [Panel(get_content(user), expand=True) for user in users]
console.print(Columns(user_renderables))

"""

Demonstrates a dynamic Layout

"""
layout = Layout()

layout.split(
    Layout(name="header", size=1),
    Layout(ratio=1, name="main"),
    Layout(size=10, name="footer"),
)

layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))

layout["side"].split(Layout(), Layout())

layout["body"].update(
    Align.center(
        Text(
            """This is a demonstration of rich.Layout\n\nHit Ctrl+C to exit""",
            justify="center",
        ),
        vertical="middle",
    )
)


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(),
                    style="bold magenta",
                    justify="center")


layout["header"].update(Clock())

with Live(layout, screen=True, redirect_stderr=False) as live:
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass


"""

Demonstrates the use of multiple Progress instances in a single Live display.

"""
job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
job1 = job_progress.add_task("[green]Cooking")
job2 = job_progress.add_task("[magenta]Baking", total=200)
job3 = job_progress.add_task("[cyan]Mixing", total=400)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid()
progress_table.add_row(
    Panel.fit(
        overall_progress,
        title="Overall Progress",
        border_style="green",
        padding=(2, 2)
    ),
    Panel.fit(job_progress,
              title="[b]Jobs",
              border_style="red",
              padding=(1, 2)),
)

with Live(progress_table, refresh_per_second=10):
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if not job.finished:
                job_progress.advance(job.id)

        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)
