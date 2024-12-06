import click
import requests
import importlib.metadata


PACKAG_NAME = "ebo-test"


@click.group()
def ebo():
    """Simple actions"""
    pass


@ebo.command()
def hello():
    """Say hello from Ebo CLI"""
    click.echo("Hello from Ebo CLI!")


@ebo.command()
@click.argument("name")
def greet(name):
    """Greet someone by name."""
    click.echo(f"Hello, {name}!")


@ebo.command()
def check():
    current_version = importlib.metadata.version(PACKAG_NAME)

    response = requests.get(
        f"https://pypi.org/pypi/{PACKAG_NAME}/json",
        headers={"Accept": "application/json"},
    )
    data = response.json()
    latest_version = data["info"]["version"]

    if current_version < latest_version:
        print(
            f"New version {latest_version} available! You're currently on {current_version}. Run pip install {PACKAG_NAME} --upgrade to upgrade! "
        )
    else:
        print(f"You're using the latest version ({current_version}).")
