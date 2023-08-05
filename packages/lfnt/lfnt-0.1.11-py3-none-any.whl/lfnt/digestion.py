import os
import platform
import subprocess
from click_configfile import ConfigFileReader, Param, SectionSchema
from click_configfile import matches_section


def run_command(command):
    command_result = None
    try:
        command_result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        pass

    return command_result


def get_config_files():
    return {}


def get_system():
    architecture, _ = platform.architecture()
    os_name = ""
    os_version = ""
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                name = line.split("=")[0]
                value = line.split("=")[1].strip()
                if name == "PRETTY_NAME":
                    os_name = value.rstrip('"').lstrip('"')
                elif name == "VERSION_CODENAME":
                    os_version = value
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_name": os_name,
        "os_version": os_version,
        "machine": platform.machine(),
        "architecture": architecture,
    }


def get_packages():
    all_packages = {}
    for pkgmgr in ["apt", "brew", "dnf"]:
        which_cmd = run_command(["which", pkgmgr])
        if which_cmd is not None and which_cmd.returncode < 1:
            if pkgmgr == "apt":
                pkgs = run_command(["apt-mark", "showmanual"])
            if pkgmgr == "brew":
                pkgs = run_command(["brew", "leaves"])
            if pkgmgr == "dnf":
                pkgs = run_command(["dnf", "list", "installed"])
            all_packages[pkgmgr] = pkgs.stdout.decode().splitlines()
    return all_packages


class LocalEnv:
    def __init__(self):
        self.system = get_system()
        self.shell = os.getenv("SHELL")
        self.packages = None

    def get(self):
        if self.packages is None:
            self.packages = get_packages()

        return {
            "system": self.system,
            "packages": self.packages,
            "shell": self.shell,
        }


le = LocalEnv()


class ConfigSectionSchema(object):
    """Describes all config sections of this configuration file."""

    @matches_section("profile")
    class Profile(SectionSchema):
        name = Param(type=str)
        email = Param(type=str)
        git_provider = Param(type=str)
        config_repo = Param(type=str)


class ConfigFileProcessor(ConfigFileReader):
    home = os.getenv("HOME")
    config_files = [f"{home}/.lfntrc"]
    config_section_schemas = [
        ConfigSectionSchema.Profile,
    ]


CONTEXT_SETTINGS = dict(default_map=ConfigFileProcessor.read_config())


class LocalProfile:
    def __init__(self):
        self.context = CONTEXT_SETTINGS["default_map"]
        self.config_files = None

    def get(self):
        if self.config_files is None:
            self.config_files = get_config_files()

        return {
            "context": self.context,
            "config_files": self.config_files,
        }


lp = LocalProfile()


class DigestiveSystem:
    def __init__(self):
        pass

    def dump(self):
        return {
            "profile": lp.get(),
            "environment": le.get(),
        }

    def get(self):
        return CONTEXT_SETTINGS

    def get_package(self, pkgmgr, pkg):
        pkg_data = run_command([pkgmgr, "info", pkg])
        return pkg_data.stdout.decode().splitlines()

    def eat_package(self, pkgmgr, pkg):
        action = "install"
        command = [pkgmgr, action, pkg]
        pkg_data = run_command(command)
        return pkg_data.stdout.decode().splitlines()

    def poop_package(self, pkgmgr, pkg):
        action = "uninstall"
        if pkgmgr in ["apt"]:
            action = "remove"
        pkg_data = run_command([pkgmgr, action, pkg])
        return pkg_data.stdout.decode().splitlines()
