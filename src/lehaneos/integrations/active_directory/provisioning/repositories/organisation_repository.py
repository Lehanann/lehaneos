from pathlib import Path
from lehaneos.integrations.active_directory.provisioning.repositories.yaml_repository import YamlRepository
from lehaneos.integrations.active_directory.provisioning.schemas.company import Company
from lehaneos.integrations.active_directory.provisioning.schemas.organization import OrganizationUnit

class OrganizationRepository(YamlRepository):
    """
    Repository responsible for accessing organization
    """
    PATH_FILE = Path(__file__).parent.parent / "config" / "organization.yaml"

    def get_company(self) -> Company | None:
        """
       Retrieve company information from the organization repository.

       Returns:
           A Company instance containing the organization details,
           otherwise None if the configuration cannot be loaded.
       """
        data = self._load()

        if data is None:
            return None

        return Company.model_validate(data["company"])

    def get_organization_unit(self, name_unit: str) -> OrganizationUnit | None:
        """
        Retrieve an organization unit by its identifier.

        Args:
            name_unit: Organization unit identifier defined in the
                organization configuration file.

        Returns:
            The matching OrganizationUnit instance if found,
            otherwise None.
        """
        data = self._load()
        if data is None:
            return None

        organization_unit = data["organization_units"].get(name_unit)
        if organization_unit is None:
            return None

        return OrganizationUnit.model_validate(organization_unit)

    def list_organization_units(self) -> list[OrganizationUnit]:
        """
        Retrieve all organization units defined in the organization
        configuration file.

        Returns:
            A list containing all configured organization units.
            Returns an empty list if the configuration cannot be loaded.
        """
        data = self._load()

        if data is None:
            return []
        return [
                OrganizationUnit.model_validate(unit)
                for unit in data["organization_units"].values()
        ]