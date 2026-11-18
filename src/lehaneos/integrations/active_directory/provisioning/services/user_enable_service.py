import logging

from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError,
    ActiveDirectoryOrganizationUnitNotFoundError, ActiveDirectoryUserNotDisabledError,
)

from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserIdentity, UserMove

logger = logging.getLogger(__name__)

class UserEnableService:

    def __init__(self, active_directory_client: ActiveDirectoryClient):
        self.active_directory_client = active_directory_client


    def enable(self, username: str, organization_unit_name: str) -> UserMove:
        """
        Build user enable payload.

        Args:
            username: Active Directory username.
            organization_unit_name: Organization unit name.
        Returns:
            UserIdentity payload.
        """
        # ======================================================
        # User Identity
        # ======================================================
        # get username on the active directory
        user = self.active_directory_client.search_user(username)
        # Check username if not exists causes an error
        if user is None:
            logger.error(
                "User '%s' does not exist in OU Disabled.",
                username,
            )
            raise ActiveDirectoryUserNotFoundError(username)

        if not user.is_disabled:
            logger.error(
                "User '%s' is not disabled in Active Directory.",
                user.username
            )
            raise ActiveDirectoryUserNotDisabledError("user is not disabled in Active Directory.")

        if not "OU=Disabled" in user.parent_ou_dn:
            logger.error(
                "User '%s' is not in OU Disabled.",
            )
            raise ActiveDirectoryUserNotDisabledError("user is not in OU Disabled.")

        # ======================================================
        # Organizational unit
        # ======================================================
        # Check organizational unit if not exists causes an error
        organizational_unit = self.active_directory_client.search_organizational_unit(organization_unit_name)
        # Check organizational unit if not exists causes an error
        if organizational_unit is None:
            logger.error(
                "Organization unit '%s' does not exist in the organizational unit toolkit.",
                organization_unit_name,
            )
            raise ActiveDirectoryOrganizationUnitNotFoundError()


        return UserMove(
            username=user.username,
            display_name=user.display_name,
            distinguished_name=user.distinguished_name,
            target_ou_dn=organizational_unit.distinguished_name,
        )