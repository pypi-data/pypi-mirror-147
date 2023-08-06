import os
import time
from pathlib import Path

import click
from flask import current_app
from flask.cli import with_appcontext

import raspcuterie
from ..config.schema import RaspcuterieConfigSchema
from ..config.setup import find_active_control_group

from ..devices import InputDevice, OutputDevice
from ..gpio import GPIO

os.environ.setdefault("FLASK_APP", "raspcuterie.app")

module_path = Path(__file__).parent


@click.group()
@click.option("--config", type=click.File(), default=None)
@click.pass_context
@click.version_option(version=raspcuterie.version)
def cli(ctx, config):

    ctx.ensure_object(dict)

    ctx.obj["config"] = config


from . import cron, fake, install  # noqa


@cli.command(short_help="Echo the current value of the input and output devices")
@with_appcontext
@click.pass_context
def devices(ctx):
    secure_pin = 24

    GPIO.setup(secure_pin, GPIO.OUT)
    GPIO.output(secure_pin, GPIO.HIGH)

    click.echo(f"Setting {secure_pin} to HIGH to activate the AM2302")

    time.sleep(1)

    click.echo("Listing input devices:")
    click.echo("============================")

    for key, device in InputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.read()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)

    click.echo("")
    click.echo("Listing output devices:")
    click.echo("============================")

    for key, device in OutputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.value()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)

    click.echo(f"Setting {secure_pin} to LOW to disable the AM2302")


@cli.command(short_help="Edit the configuration file")
def config():

    file = raspcuterie.base_path / "config.yaml"

    if not raspcuterie.base_path.exists():
        raspcuterie.base_path.mkdir(parents=True)

    if not file.exists():
        x = module_path / "config.yaml"
        with file.open("w") as f:
            f.write(x.read_text())

    click.echo(f"Editing {file} ")
    click.edit(filename=file)


@cli.command(short_help="Version number")
def version():
    click.echo(raspcuterie.version)

    file = raspcuterie.base_path / "config.yaml"

    click.echo(f"Config: {file} ")


@cli.command(short_help="Write schema to raspcuterie.json")
@click.option("--file", type=click.File(mode="w"))
def schema(file=None):

    if file is None:
        file = Path("raspcuterie.schema.json")

    from ..config.schema import RaspcuterieConfigSchema

    RaspcuterieConfigSchema.update_forward_refs()
    file.write_text(RaspcuterieConfigSchema.schema_json())

    click.echo(f"Schema written to {file.absolute()}")


@cli.command(short_help="Display the rules of the active control group")
@with_appcontext
def control_rules():

    config_schema: RaspcuterieConfigSchema = current_app.schema

    x = find_active_control_group(config_schema.control)

    if x is not None:
        name, group = x

        click.echo(f"Active control group: {name} and expires {group.expires}")

        for device, rules in group.rules.items():
            click.echo(device)

            for rule in rules:
                click.echo(f"{rule.rule} {rule.expression} {rule.action}")
