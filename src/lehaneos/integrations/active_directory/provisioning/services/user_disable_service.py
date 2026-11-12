import logging

from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError
)

from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserIdentity

logger = logging.getLogger(__name__)

class UserDisableService:

    def __init__(self, active_directory_client: ActiveDirectoryClient):
        self.active_directory_client = active_directory_client

    def disable(self, username: str) -> UserIdentity:
        """
        Build user disable payload.

        Args:
            username: Active Directory username.

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
                "User '%s' does not exist in Active Directory.",
                username,
            )
            raise ActiveDirectoryUserNotFoundError(f"User not found.")

        return UserIdentity(
            username=user.username,
        )