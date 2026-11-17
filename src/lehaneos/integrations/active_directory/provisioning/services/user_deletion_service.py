import logging

from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError,
    ActiveDirectoryOrganizationUnitNotFoundError,
)

from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserIdentityLifecycle

logger = logging.getLogger(__name__)

class UserDeletionService:
    def __init__(self, active_directory_client: ActiveDirectoryClient) -> None:
        self.active_directory_client = active_directory_client

    def delete(self, username: str, organization_unit_name: str) -> UserIdentityLifecycle:
        """
        Build user deletion payload.

        Args:
            username: Active Directory username.
            organization_unit_name: Active Directory organization unit name.
        Returns:
            UserIdentityLifecycle payload.
        """
        # ======================================================
        # Organizational unit
        # ======================================================
        #Check organizational unit if not exists causes an error
        if not self.active_directory_client.organizational_unit_exists(organization_unit_name):
            logger.error(
                "Organization unit '%s' does not exist in Active Directory.",
                organization_unit_name,
            )
            raise ActiveDirectoryOrganizationUnitNotFoundError()

        # ======================================================
        # User Identity
        # ======================================================
        # get username on the active directory
        user = self.active_directory_client.search_user_ou(username,organization_unit_name)
        # Check username if not exists causes an error
        if user is None:
            logger.error(
                "User '%s' does not exist in Disabled OU.",
                username,
            )
            raise ActiveDirectoryUserNotFoundError(f"User not found.")

        if not self.active_directory_client.is_disabled(user.username):
            logger.error(
                "User '%s' is not disabled in Disabled OU.",
                username,
            )
            raise ActiveDirectoryUserNotFoundError(f"User not found.")

        return UserIdentityLifecycle(
            username=user.username,
            display_name=user.display_name,
            distinguished_name=user.distinguished_name,
            target_ou_dn=organization_unit_name
        )
