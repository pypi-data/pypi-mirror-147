import pathlib

import pkg_resources
from pkg_resources import DistributionNotFound

base_path = pathlib.Path(__file__).parent.parent


def get_version():
    try:
        return pkg_resources.require("raspcuterie")[0].version
    except DistributionNotFound:
        return "dev"


version = get_version()
