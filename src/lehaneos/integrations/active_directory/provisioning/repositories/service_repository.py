from pathlib import Path

from lehaneos.integrations.active_directory.provisioning.repositories.yaml_repository import (
    YamlRepository,
)
from lehaneos.integrations.active_directory.provisioning.schemas.service import Service


class ServiceRepository(YamlRepository):
    """
    Repository responsible for accessing services.
    """

    PATH_FILE = Path(__file__).parent.parent / "config" / "service.yaml"

    def get_service(self, service_name: str ) -> Service | None:
        """
        Retrieve a service definition by its identifier.

        Args:
            service_name: Service identifier defined
                in the service configuration file.

        Returns:
            The matching Service instance if found,
            otherwise None.
        """
        data = self._load()

        if data is None:
            return None

        service = data["services"].get(service_name)

        if service is None:
            return None

        return Service.model_validate(service)

    def list_services(self) -> list[Service]:
        """
        Retrieve all services defined in the service
        configuration file.

        Returns:
            A list containing all configured services.
            Returns an empty list if the configuration
            cannot be loaded.
        """
        data = self._load()

        if data is None:
            return []

        return [
            Service.model_validate(service)
            for service in data["services"].values()
        ]