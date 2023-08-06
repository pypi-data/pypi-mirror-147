from datetime import datetime, timedelta

from raspcuterie.config.schema import ControlGroupSchema
from raspcuterie.config.setup import find_active_control_group


def test_find_active_control_group():

    control_groups = dict(
        x=ControlGroupSchema(expires=datetime.now() + timedelta(days=3), rules={}),
        y=ControlGroupSchema(expires=datetime.now() + timedelta(days=1), rules={}),
        z=ControlGroupSchema(expires=datetime.now() + timedelta(days=2), rules={}),
    )

    assert find_active_control_group(control_groups)[0] == "y"


def test_find_active_control_group_with_default():

    control_groups = dict(
        x=ControlGroupSchema(expires=datetime.now() + timedelta(days=3), rules={}),
        y=ControlGroupSchema(expires=datetime.now() + timedelta(days=1), rules={}),
        z=ControlGroupSchema(expires=datetime.now() + timedelta(days=2), rules={}),
        d=ControlGroupSchema(expires=None, rules={}),
    )

    assert find_active_control_group(control_groups)[0] == "d"
