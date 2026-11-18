import logging

from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError,
    ActiveDirectoryUserNotDisabledError,
)

from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserIdentity

logger = logging.getLogger(__name__)

class UserDeletionService:
    def __init__(self, active_directory_client: ActiveDirectoryClient) -> None:
        self.active_directory_client = active_directory_client

    def delete(self, username: str) -> UserIdentity:
        """
        Build user deletion payload.

        Args:
            username: Active Directory username.

        Returns:
            UserIdentityLifecycle payload.
        """
        # ======================================================
        # User Identity
        # ======================================================
        # get username on the active directory
        user = self.active_directory_client.search_user(username)
        # Check username if not exists causes an error
        if user is None:
            logger.error(
                "User '%s' does not exist in Active directory.",
                username,
            )
            raise ActiveDirectoryUserNotFoundError(f"User not found.")

        if not user.is_disabled:
            logger.error(
                "User '%s' is not disabled in Active Directory.",
            )
            raise ActiveDirectoryUserNotDisabledError(f"User is not disabled.")

        if "OU=Disabled" not in user.parent_ou_dn:
            logger.error(
                "User '%s' is not to OU=Disabled in Active Directory.",
            )
            raise ActiveDirectoryUserNotDisabledError(f"User is not to OU=Disabled.")

        return UserIdentity(
            username=user.username,
            display_name=user.display_name,
            distinguished_name=user.distinguished_name,
        )
