from lehaneos.settings.settings import settings


class AccountMembershipBuilder:
    def build_groups_dn(self, groups: list[str]) -> list[str]:
        """
        Build a Distinguished Name(DN) for each group

        Args:
            groups (list[str]): List of groups

        Returns:
            list[str]: Distinguished Name(DN) built for each group.
        """
        groups_dn: list[str] = []
        for group in groups:
            groups_dn.append(f"{group},{settings.ad_groups_dn}")
        return groups_dn

    def build_organization_unit(self, role_user: str) -> str:
        """
        Build an organization unit for a role user.

        Args:
            role_user: Role user to build the organization unit.

        Returns:
            built organization unit for a role user.
        """
        return f"OU={role_user},{self.AD_FULL_ROOT}"
