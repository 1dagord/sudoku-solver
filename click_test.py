#! .venv/bin/python3.13

import click

all_colors = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
)

@click.command()
def cli():
    for color in all_colors:
        click.echo(click.style(f"I am colored {color}", fg=color))
        
    click.echo(click.style("I am blinking", blink=True))


if __name__ == "__main__":
    cli()
