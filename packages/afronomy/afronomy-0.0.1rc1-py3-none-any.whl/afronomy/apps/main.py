import sys
import click
from .hello import main


@click.group()
def driver():
    """Top-level CLI for Afronomy."""
    pass

# Add hello CLI as a subcommand to driver
driver.add_command(main, "hello")

if __name__ == "__main__":
    sys.exit(driver())
