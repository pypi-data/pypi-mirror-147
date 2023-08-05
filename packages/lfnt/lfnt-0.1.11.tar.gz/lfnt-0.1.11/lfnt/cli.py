import click
from pprint import pprint
from .app import app
from .digestion import DigestiveSystem


de = DigestiveSystem()
CONTEXT_SETTINGS = de.get()


@click.group(context_settings=CONTEXT_SETTINGS)
def lfnt():
    """For eating development-environment elephants."""
    pass


lfnt_group = lfnt.group(context_settings=CONTEXT_SETTINGS)
lfnt_command = lfnt.command(context_settings=CONTEXT_SETTINGS)


# browse
@lfnt_command
def browse():
    """Run in a web browser."""
    app.run()


# life-cycle
@lfnt_command
def init():
    """Initialize a configuration."""
    pass


# digestion
@lfnt_command
@click.option("-a", "--apt", multiple=True)
@click.option("-b", "--brew", multiple=True)
@click.option("-d", "--dnf", multiple=True)
def eat(apt, brew, dnf):
    """Ingest packages and applications."""
    for pkg in apt:
        print(de.eat_package("apt", pkg))
    for pkg in brew:
        print(de.eat_package("brew", pkg))
    for pkg in dnf:
        print(de.eat_package("dnf", pkg))


@lfnt_command
@click.option("-a", "--apt", multiple=True)
@click.option("-b", "--brew", multiple=True)
@click.option("-d", "--dnf", multiple=True)
def poop(apt, brew, dnf):
    """Eliminate packages and applications."""
    for pkg in apt:
        print(de.poop_package("apt", pkg))
    for pkg in brew:
        print(de.poop_package("brew", pkg))
    for pkg in dnf:
        print(de.poop_package("dnf", pkg))


@lfnt_command
def remember():
    """Save and commit environment."""
    pass


@lfnt_command
def dump():
    """Take a config dump."""
    pprint(de.dump())


if __name__ == "__main__":
    lfnt()
