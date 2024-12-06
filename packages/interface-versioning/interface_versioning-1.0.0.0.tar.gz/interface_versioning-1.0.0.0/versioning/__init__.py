__all__ = ["FailedRequirement", "Version", "register", "require"]

from .numbers import *
from .requirements import *

register(Version, "versioning.VersionFactory", "1.0.0")
register(Version, "versioning.VersionParser", "1.0.0")

import sys
register(sys.modules[__name__], "versioning", "1.0.0")
