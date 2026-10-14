from lehaneos.core.exceptions.base import LehaneosError

class ActiveDirectoryError(LehaneosError):
    pass

class ActiveDirectoryConnectionError(ActiveDirectoryError):
    pass

class ActiveDirectorySearchError(ActiveDirectoryError):
    pass

