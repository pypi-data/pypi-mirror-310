import click

@click.group()
def ebo():
    """Ebo Command Line Interface"""
    pass

@ebo.command()
def hello():
    """Say hello from Ebo CLI"""
    click.echo("Hello from Ebo CLI!")

@ebo.command()
@click.argument('name')
def greet(name):
    """Greet someone by name."""
    click.echo(f"Hello, {name}!")