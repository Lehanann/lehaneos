import logging

from lehaneos.integrations import active_directory
from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError,
    ActiveDirectoryUserAlreadyDisabledError, ActiveDirectoryOrganizationUnitNotFoundError
)
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.repositories.organisation_repository import \
    OrganizationRepository
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserMove

logger = logging.getLogger(__name__)

class UserDisableService:

    def __init__(
            self,
            active_directory_client: ActiveDirectoryClient,
            organization_repository: OrganizationRepository,
    ) -> None:
        self.active_directory_client = active_directory_client
        self.organization_repository = organization_repository


    def disable(self, username: str, organizational_unit_name: str) -> UserMove:
        """
        Build user disable payload.

        Args:
            username: Active Directory username.
            organizational_unit_name: Active Directory organizational unit name.

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

        if user.is_disabled:
            logger.error(
                "User '%s' is already disabled in Active Directory.",
                user.username
            )
            raise ActiveDirectoryUserAlreadyDisabledError(f"User is already disabled in Active Directory.")

        if "OU=Disabled" in user.parent_ou_dn:
            logger.error(
                "User '%s' is in OU Disabled in Active Directory.",
                user.username,
            )
            raise ActiveDirectoryUserAlreadyDisabledError(f"User is in OU Disabled in Active Directory.")

        # ======================================================
        # Organizational unit
        # ======================================================
        #Check organizational unit if not exists causes an error
        organizational_unit = self.active_directory_client.search_organizational_unit(organizational_unit_name)

        if organizational_unit is None:
            logger.error(
                "Organization unit '%s' does not exist in Active Directory.",
                organizational_unit_name,
            )
            raise ActiveDirectoryOrganizationUnitNotFoundError(f"Organization unit not found.")

        return UserMove(
            username=user.username,
            display_name=user.display_name,
            distinguished_name=user.distinguished_name,
            target_ou_dn=organizational_unit.distinguished_name,
        )