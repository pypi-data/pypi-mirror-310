#!/usr/bin/env python
import os
import sys
import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

@click.group()
def main():
    """CLI entry point."""
    pass

@main.command()
@click.option('--name', prompt='Please enter your name', help='The name to greet.')
def hello(name):
    """CLI entry point."""
    click.echo(_hello(name))

def _hello(name: str) -> str:
    """Function that returns a greeting string."""
    return f"Hello {name}"

schemas = OmegaConf.load(os.path.join(os.path.dirname(__file__), "../cabs/hello.yml"))

def clickify(name, schema_name=None):
    schema_name = schema_name or name
    return lambda func: \
        main.command(name, help=schemas.cabs.get(f'afronomy.{schema_name}').info,no_args_is_help=True)(
                clickify_parameters(schemas.cabs.get(f'afronomy.{schema_name}'))(func)
        )

