import subprocess
import json
from pathlib import Path
import logging
from lehaneos.core.logging_config import configure_logging
from lehaneos.core.exceptions.base import PowershellError

logger = logging.getLogger(__name__)


class PowerShellRunner:

    def run(self, script: Path, parameters: dict):
        """
        Execute a PowerShell script and parse
        its JSON response.

        Args:
            script: Full path of the PowerShell script.
            parameters: Arguments passed to the script.

        Returns:
            dict: Parsed JSON response.

        Raises:
            PowerShellError: If the script execution
            fails or if the returned JSON is invalid.
        """

        script_name= Path(script).stem

        logger.info(f"Launching Powershell script")
        logger.info(f"Script: {script}")
        logger.info(f"Arguments: {parameters}")

        params_build = self._build_arguments(parameters)
        pwsh_command = subprocess.run(
            [
                "pwsh",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                script,
                *params_build,
            ],
            capture_output=True,
            text=True
        )

        logger.info(f"Return code: {pwsh_command.returncode}")

        if pwsh_command.stderr:
            logger.error(f"Stderr: {pwsh_command.stderr}")

        try:
            response = json.loads(pwsh_command.stdout)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {pwsh_command.stdout}")
            raise PowershellError("Invalid JSON returned by Powershell")

        log_message = (f"Module: {script_name} - {response['code']} - {response['message']}")

        match response["status"]:
            case "success":
                logger.info(log_message)

            case "warning":
                logger.warning(log_message)

            case "error":
                logger.error(log_message)
                raise PowershellError(response["message"])
            case _:
                logger.error(
                    f"Unknown status returned: {response}"
                )
                raise PowershellError(
                    "Unknown status returned by Powershell"
        )


        return response

    def _build_arguments(self, parameters: dict) -> list[str]:
        build_parameters = []
        for key, value in parameters.items():
            build_parameters.append(f"-{key}")
            if isinstance(value, list):
                for item in value:
                    build_parameters.append(item)
            else:
                build_parameters.append(value)

        return build_parameters