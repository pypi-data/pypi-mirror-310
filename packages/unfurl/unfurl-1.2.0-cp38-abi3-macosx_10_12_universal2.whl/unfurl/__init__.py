# SPDX-License-Identifier: MIT
# Copyright (c) 2020 Adam Souzis
import logging
import os
import sys
from typing import Dict, Optional, Union, TYPE_CHECKING

import pbr.version

from . import logs


# We need to initialize logging before any logger is created
logs.initialize_logging()


def __version__(include_prerelease: bool = False) -> str:
    # this is expensive so make this a function to calculate lazily
    if include_prerelease:
        # if running from a repository appends .devNNN using something like git describe
        return pbr.version.VersionInfo(__name__).release_string()
    else:  # semver only (last release)
        return pbr.version.VersionInfo(__name__).version_string()


def semver_prerelease() -> str:
    bpr_ver = __version__(True)
    parts = bpr_ver.split(".")
    # if ends with .devNNN, bump the patch version to indicate upcoming release and append pre-release version
    if len(parts) > 3:
        return f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}-dev.{parts[3].lstrip('dev')}"
    else:
        return bpr_ver


def version_tuple(v: Union[None, str] = None) -> tuple:
    "Convert a pbr or semver version string into a comparable 3 or 4 item tuple."
    if v is None:
        v = __version__(True)
    elif "-" in v:  # its a semver with a pre-release version
        v, sep, prerelease = v.partition("-")
        semver = version_tuple(v)
        prerelease, sep, build_id = prerelease.partition("+")
        # decrement patch version and add prerelease as an int so it compares properly with released version
        return semver[0:2] + (semver[2] - 1, int(prerelease.lstrip("dev.") or 0))
    elif "+" in v:
        v, sep, build_id = v.partition("+")
    return tuple(int(x.lstrip("dev") or 0) for x in v.split("."))


def is_version_unreleased(v: Union[None, str] = None) -> bool:
    return len(version_tuple(v)) > 3


_vendor_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "vendor")
sys.path.insert(0, _vendor_dir)
_vendor_dir2 = os.path.join(_vendor_dir, "tosca", "vendor")
sys.path.insert(0, _vendor_dir2)

_tosca_types = [
    "nodes",
    "capabilities",
    "relationships",
    "interfaces",
    "datatypes",
    "artifacts",
    "groups",
]
__safe__ = _tosca_types


class DefaultNames:
    SpecDirectory = "spec"
    EnsembleDirectory = "ensemble"
    Ensemble = "ensemble.yaml"
    EnsembleTemplate = "ensemble-template.yaml"
    ServiceTemplate = "service_template.yaml"
    LocalConfig = "unfurl.yaml"
    SecretsConfig = "secrets.yaml"
    HomeDirectory = ".unfurl_home"
    JobsLog = "jobs.tsv"
    ProjectDirectory = ".unfurl"
    LocalConfigTemplate = ".unfurl-local-template.yaml"
    InputsTemplate = "inputs-template.yaml"

    def __init__(self, **names: Optional[str]) -> None:
        self.__dict__.update({name: value for name, value in names.items() if value})


DEFAULT_CLOUD_SERVER = "https://unfurl.cloud"


def get_home_config_path(homepath: Union[None, str]) -> Union[None, str]:
    # if homepath is explicitly it overrides UNFURL_HOME
    # (set it to empty string to disable the homepath)
    # otherwise use UNFURL_HOME or the default location
    if homepath is None:
        if "UNFURL_HOME" in os.environ:
            homepath = os.getenv("UNFURL_HOME")
        else:
            homepath = os.path.join("~", DefaultNames.HomeDirectory)
    if homepath:
        homepath = os.path.expanduser(homepath)
        if not os.path.exists(homepath):
            isdir = not homepath.endswith(".yml") and not homepath.endswith(".yaml")
        else:
            isdir = os.path.isdir(homepath)
        if isdir:
            return os.path.abspath(os.path.join(homepath, DefaultNames.LocalConfig))
        else:
            return os.path.abspath(homepath)
    return None


__all__ = [
    "DefaultNames",
    "get_home_config_path",
    "is_version_unreleased",
    "version_tuple",
    # same as _tosca_types (but __all__ can't be an expression):
    "nodes",
    "capabilities",
    "relationships",
    "interfaces",
    "datatypes",
    "artifacts",
    "groups",
]

### Ansible initialization
if "ANSIBLE_CONFIG" not in os.environ:
    os.environ["ANSIBLE_CONFIG"] = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "configurators", "ansible.cfg")
    )
try:
    import ansible
except ImportError:
    pass
else:
    import ansible.constants as C

    if "ANSIBLE_NOCOWS" not in os.environ:
        C.ANSIBLE_NOCOWS = 1
    if "ANSIBLE_JINJA2_NATIVE" not in os.environ:
        C.DEFAULT_JINJA2_NATIVE = 1

    import ansible.utils.display

    ansible.utils.display.logger = logging.getLogger("unfurl.ansible")
    display = ansible.utils.display.Display()

    # Display is a singleton which we can't subclass so monkey patch instead
    _super_display = ansible.utils.display.Display.display

    def _display(
        self: ansible.utils.display.Display.display,
        msg: str,
        color: Union[None, str] = None,
        stderr: bool = False,
        screen_only: bool = False,
        log_only: bool = True,
        newline: bool = True,
        **kw,
    ) -> Union[None, ansible.utils.display.Display]:
        if screen_only:
            return None
        return _super_display(
            self, msg, color, stderr, screen_only, log_only, newline, **kw
        )

    ansible.utils.display.Display.display = _display

    from ansible.plugins.loader import filter_loader, lookup_loader

    lookup_loader.add_directory(os.path.abspath(os.path.dirname(__file__)), True)
    filter_loader.add_directory(os.path.abspath(os.path.dirname(__file__)), True)

# these need to be imported after DEFAULT_JINJA2_NATIVE is set:

from .tosca_plugins.tosca_ext import nodes
from .tosca_plugins.tosca_ext import interfaces
from .tosca_plugins.tosca_ext import relationships
from .tosca_plugins.tosca_ext import capabilities
from .tosca_plugins.tosca_ext import datatypes
from .tosca_plugins.tosca_ext import artifacts
from .tosca_plugins.tosca_ext import groups
