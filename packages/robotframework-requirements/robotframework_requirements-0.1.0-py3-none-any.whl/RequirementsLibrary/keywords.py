"""Keywords for robotframework-requirements library"""
import pathlib
from collections import namedtuple

import pkg_resources  # type: ignore
from packaging import version
from robot.api import logger  # type: ignore
from robot.api.deco import keyword  # type: ignore

Package = namedtuple("Package", "name operator version")


class RequirementsKeywords:
    # pylint: disable=too-few-public-methods
    """Class for warning users of incorrect library versions.

    This is instantiated as class so it is run in beginning of test suite

    *Examples*

    | Library | RequirementsLibrary |
    | Library | RequirementsLibrary | ${CURDIR}/../requirements.txt |
    """

    def __init__(self, requirements_path="requirements.txt") -> None:
        logger.debug("Starting robotframework-requirements")
        self.requirements = _get_requirements(requirements_path)
        self.installed = _get_installed()
        _compare_versions(self.requirements, self.installed)
        logger.debug("End robotframework-requirements")

    @keyword
    def check_libraries(self, requirements_path="requirements.txt") -> bool:
        """Check robot framework library versions.

        *Examples*

        | Check Libraries |
        | Check Libraries | ${CURDIR}/../requirements.txt |
        """
        success = True
        if requirements_path != "":
            self.requirements = _get_requirements(requirements_path)
        success = _compare_versions(self.requirements, self.installed)
        if success is False:
            raise Exception("Packages have incorrect versions or are missing. Check logs")
        return True


def _compare_versions(requirements: list, installed: list):
    """Compare required packages list against installed packages"""
    success = True
    for package in requirements:
        if _compare_version(package, installed) is False:
            success = False
    return success


def _compare_version(package: Package, installed_list: list) -> bool:
    """Compare a package against a list of packages"""
    success = True
    installed = _get_installed_version(package.name, installed_list)
    if installed is None:
        success = False
        message = f"Required package {package.name} not found"
    elif package.operator == "==":
        if package.version != installed.version:
            success = False
            message = (
                f"Package {package.name} should be {package.version}, " f"is {installed.version}"
            )
    elif package.operator == ">=":
        if package.version > installed.version:
            success = False
            message = (
                f"Package {package.name} should be {package.version} "
                f"or later, is {installed.version}"
            )
    else:
        message = f"Unknown operator in requirements.txt: {package.operator}"
        success = False
    if success is False:
        logger.warn(message)
    return success


def _get_installed_version(name, installed_list):
    """Return installed version of package"""
    try:
        return [x for x in installed_list if x.name == name][0]
    except IndexError:
        return None


def _get_requirements(requirements_path="requirements.txt") -> list:
    """Return list of required packages from requirements file."""
    install_requires_list = []
    try:
        with pathlib.Path(requirements_path).open(encoding="utf-8") as requirements_txt:
            install_requires_list = [
                _make_package(str(requirement))
                for requirement in pkg_resources.parse_requirements(requirements_txt)
            ]
    except FileNotFoundError as filenotfound_error:
        raise Exception(f"Cannot find file {requirements_path}") from filenotfound_error
    logger.debug(f"Loaded {len(install_requires_list)}requirements")
    return install_requires_list


def _get_installed() -> list:
    """Return list of installed packages."""
    installed_packages = pkg_resources.working_set.__iter__()
    installed_packages_list = sorted(
        [Package(i.key, "==", version.parse(i.version)) for i in installed_packages]
    )
    logger.debug(f"Found {len(installed_packages_list)} installed packages")
    return installed_packages_list


def _make_package(package_str: str) -> Package:
    """Create a Package object from package string."""
    if "==" in package_str:
        name, installed_version = package_str.split("==")
        operator = "=="
    elif ">=" in package_str:
        name, installed_version = package_str.split(">=")
        operator = ">="
    else:
        name = package_str
        installed_version = "0.0.0"
        operator = ">="
    return Package(name.lower(), operator, version.parse(installed_version))
