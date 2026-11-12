import logging

from lehaneos.core.security.password_generator import PasswordGenerator

from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError
)
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserResetPassword

logger = logging.getLogger(__name__)

class UserResetPasswordService:

    def __init__(self, active_directory_client: ActiveDirectoryClient):
        self.active_directory_client = active_directory_client

    def reset_password(self, username: str) -> UserResetPassword:
        """
        Build user password reset payload.

        Args:
            username: Active Directory username.

        Returns:
            UserResetPassword payload.
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

        return UserResetPassword(
            username=user.username,
            new_password=PasswordGenerator().generate()
        )