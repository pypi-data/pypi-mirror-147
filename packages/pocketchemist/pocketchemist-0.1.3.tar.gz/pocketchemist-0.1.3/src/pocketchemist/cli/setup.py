"""
Setup CLI subcommand
"""
from inspect import isabstract
from itertools import groupby

import click

from .hookimpls import clihook
from ..processors import Processor
from ..modules import Module
from ..utils.classes import all_subclasses


@clihook
def add_command(root_command):
    """Plugin hook to add the setup cli sub-command"""
    root_command.add_command(setup)


@click.group()
def setup():
    """Print information on the current setup"""
    pass

@setup.command()
@click.option('--only-concrete',
              is_flag=True, default=False,
              help="Only show concrete (non-abstract) classes")
def processors(only_concrete):
    """List the available processors"""
    # Retrieve a list of all processor classes
    processor_clses = all_subclasses(Processor)

    # Retrieve only concrete classes--remove abstract classes--if specified
    if only_concrete:
        processor_clses = [processor_cls
                           for processor_cls in processor_clses
                           if isabstract(processor_cls)]

    for count, processor_cls in enumerate(processor_clses, 1):
        click.echo(f"{count}. {processor_cls}")

@setup.command()
def modules():
    """List the available Python modules"""
    # Retrieve a list of all module instances
    module_objs = Module.list_instances()

    # Group by category
    modules_by_category = sorted(module_objs, key=lambda m: m.category)
    modules_by_category = groupby(modules_by_category,
                                  key=lambda m: m.category)

    for category, module_objs in modules_by_category:
        click.echo(click.style("Category: ", bold=True) + category)

        for count, module_obj in enumerate(module_objs, 1):
            module_obj.print()
