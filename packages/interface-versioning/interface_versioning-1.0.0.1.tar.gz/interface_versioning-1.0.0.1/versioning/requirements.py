__all__ = ["FailedRequirement", "register", "require"]

from .numbers import Version

class FailedRequirement(AssertionError):
    pass

if __debug__:
    def register(obj, interface: str, version: str) -> None:
        try:
            interfaces = obj.__interfaces__
        except AttributeError:
            interfaces = {}
            obj.__interfaces__ = interfaces

        try:
            versions = interfaces[interface]
        except KeyError:
            versions = set()
            interfaces[interface] = versions

        versions.add(Version.parse(version))

    def require(obj, interface: str, version: str) -> None:
        try:
            versions = obj.__interfaces__[interface]
        except (AttributeError, KeyError) as err:
            raise FailedRequirement(obj, interface, version) from err
        else:
            versionNumber = Version.parse(version)

            for registered in versions:
                if (versionNumber.major == registered.major
                and not registered < versionNumber):
                    return
            else:
                raise FailedRequirement(obj, interface, version)
else:
    def register(obj, interface: str, version: str) -> None: pass
    def require(obj, interface: str, version: str) -> None: pass
