import logging
import sys
import time
from functools import wraps
from pprint import pprint

from flask import current_app


from raspcuterie import version
from raspcuterie.cli import cli, with_appcontext
from raspcuterie.devices import InputDevice, OutputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.gpio import GPIO

if sys.platform.startswith("win"):

    def timeout(*args, **kwargs):
        def decorate(function):
            @wraps(function)
            def new_function(*args, **kwargs):
                return function(*args, **kwargs)

            return new_function

        return decorate


else:
    from timeout_decorator import timeout


def evaluate_config_rules(context):
    for rule in ControlRule.registry:
        try:
            rule.execute_if_matches(context)
        except Exception as e:
            current_app.logger.exception(e)


@cli.command(short_help="Log the input and output devices")
@with_appcontext
@timeout(30)
def log():
    current_app.logger.info(version)

    current_app.logger.setLevel(logging.DEBUG)

    secure_pin = 24
    current_app.logger.info(f"Setting {secure_pin} to HIGH to activate the AM2302")

    GPIO.setup(secure_pin, GPIO.OUT)
    GPIO.output(secure_pin, GPIO.HIGH)

    time.sleep(1)

    context = ControlRule.context()

    pprint(context)

    evaluate_config_rules(context)

    for input_device in InputDevice.registry.values():
        try:
            input_device.log()
        except Exception as e:
            current_app.logger.exception(e)

    for output_device in OutputDevice.registry.values():
        try:
            output_device.log()
        except Exception as e:
            current_app.logger.exception(e)

    GPIO.output(24, GPIO.LOW)

    current_app.logger.info(f"Setting {secure_pin} to LOW to disable the AM2302")


if __name__ == "__main__":
    log()
