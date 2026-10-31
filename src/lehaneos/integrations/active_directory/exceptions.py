from lehaneos.core.exceptions.base import LehaneosError

class ActiveDirectoryError(LehaneosError):
    pass

class ActiveDirectoryConnectionError(ActiveDirectoryError):
    pass

class ActiveDirectorySearchError(ActiveDirectoryError):
    pass

class ActiveDirectoryUserNotFoundError(ActiveDirectoryError):
    pass

class ActiveDirectoryGroupNotFoundError(ActiveDirectoryError):
    pass

class ActiveDirectoryUserAlreadyExistsError(ActiveDirectoryError):
    pass

class ActiveDirectoryJobNotFoundError(ActiveDirectoryError):
    pass

class ActiveDirectoryDomainNotFoundError(ActiveDirectoryError):
    pass

class ActiveDirectoryCompanyNotFoundError(ActiveDirectoryError):
    pass

class ActiveDirectoryOrganizationUnitNotFoundError(ActiveDirectoryError):
    pass