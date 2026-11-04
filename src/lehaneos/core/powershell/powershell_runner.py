import subprocess
import json
from pathlib import Path
import logging
from lehaneos.core.exceptions.base import PowershellError

logger = logging.getLogger(__name__)


class PowerShellRunner:

    def __init__(self, host: str, username: str):
        self.host = host
        self.username = username

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

        print("PARAMETERS BEFORE BUILD:",parameters)
        params_build = self._build_arguments(parameters)

        print("PARAMS_BUILD",params_build)

        pwsh_command = subprocess.run(
            [
                "ssh",
                "-i",
                "/home/ygrondin/.ssh/lehaneos_ad",
                f"{self.username}@{self.host}",
                "powershell.exe",
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
            print("RETURN CODE:", pwsh_command.returncode)
            print("STDOUT:", repr(pwsh_command.stdout))
            print("STDERR:", repr(pwsh_command.stderr))
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
            if isinstance(value, list):
                values = ",".join(f'"{item}"' for item in value)
                build_parameters.append(f'-{key} {values}')
            else:
                build_parameters.append(f'-{key} "{value}"')

        return build_parameters