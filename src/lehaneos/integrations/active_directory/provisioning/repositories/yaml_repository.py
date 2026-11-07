import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class YamlRepository:
    PATH_FILE = Path

    def _load(self) -> dict | None:
        """
        Load and parse the organization configuration file.

        Returns:
            A dictionary containing the YAML configuration data if the
            file is successfully loaded, otherwise None.
        """
        try:
            with open(self.PATH_FILE, "r") as file:
                config = yaml.safe_load(file)
                if config is None:
                    return None

                return config
        except FileNotFoundError:
            logger.error(
                "Organization configuration file not found: %s", self.PATH_FILE
            )
            return None
        except yaml.YAMLError as exc:
            logger.error("Unable to read organization.yaml: %s", exc)
            return None
