import logging

from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserNotFoundError,
    ActiveDirectoryOrganizationUnitNotFoundError
)
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.repositories.organisation_repository import \
    OrganizationRepository
from lehaneos.integrations.active_directory.provisioning.schemas.user_identity import UserIdentityLifecycle
from lehaneos.settings.settings import settings

logger = logging.getLogger(__name__)

class UserDisableService:

    def __init__(
            self,
            active_directory_client: ActiveDirectoryClient,
            organization_repository: OrganizationRepository,
    ) -> None:
        self.active_directory_client = active_directory_client
        self.organization_repository = organization_repository


    def disable(self, username: str, organization_unit_name: str) -> UserIdentityLifecycle:
        """
        Build user disable payload.

        Args:
            username: Active Directory username.
            organization_unit_name: Active Directory organization unit name.
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
        # ======================================================
        # Organization_Unit
        # ======================================================

        if not self.active_directory_client.organizational_unit_exists(organization_unit_name):
            logger.error(
                "Organization unit '%s' does not exist in Active Directory.",
                organization_unit_name,
            )
            raise ActiveDirectoryOrganizationUnitNotFoundError()

        organization_unit = self.organization_repository.get_organization_unit(organization_unit_name)
        if organization_unit is None:
            logger.error(
                "Organization unit '%s' does not exist in the organizational unit toolkit.",
                organization_unit_name,
            )
            raise ActiveDirectoryOrganizationUnitNotFoundError(f"Organization unit not found.")

        organization_unit_dn = f"OU={organization_unit.ou_name},{settings.full_root_ou}"

        return UserIdentityLifecycle(
            username=user.username,
            display_name=user.display_name,
            distinguished_name=user.distinguished_name,
            target_ou_dn=organization_unit_dn
        )