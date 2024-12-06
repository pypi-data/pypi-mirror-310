# pylint: disable=wrong-import-position

from __future__ import annotations


def verify_python_version() -> None:
    import platform
    import sys

    if sys.version_info < (3, 9):
        print(
            """Bikeshed now requires Python 3.9; you are on {}.
    If you're seeing this message in your CI run, you are
    likely specifying an old OS; try `ubuntu-latest`.
    If you're seeing this on the command line, see the docs
    for instructions:
    https://speced.github.io/bikeshed/#installing""".format(
                platform.python_version(),
            ),
        )
        sys.exit(1)


verify_python_version()


def verify_requirements() -> None:
    import os
    import sys

    import pkg_resources

    requirements_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "requirements.txt",
    )
    if os.path.exists(requirements_file_path):
        requirements_met = True
        with open(requirements_file_path, encoding="utf-8") as requirements_file:
            requirements = [line for line in requirements_file.read().split("\n") if (not line.strip().startswith("-"))]
            for requirement in pkg_resources.parse_requirements(requirements):
                try:
                    distribution = pkg_resources.get_distribution(requirement.project_name)
                    if distribution not in requirement:
                        print(
                            "Package {} version {} is not supported.".format(
                                requirement.project_name,
                                distribution.version,
                            ),
                        )
                        requirements_met = False
                except Exception:
                    print(f"Package {requirement.project_name} is not installed.")
                    requirements_met = False
        if not requirements_met:
            print('Run "pip3 install -r {}" to complete installation'.format(requirements_file_path))
            sys.exit(1)


verify_requirements()

from . import (
    config,
    update,
)
from .cli import main
from .Spec import Spec
