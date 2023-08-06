"""A library for verifying installed packages against requirements."""
#  pylint: disable=invalid-name
from .keywords import RequirementsKeywords
from .version import VERSION


class RequirementsLibrary(RequirementsKeywords):
    # pylint: disable=too-few-public-methods
    """Requirements verification library for Robot Framework"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = VERSION
