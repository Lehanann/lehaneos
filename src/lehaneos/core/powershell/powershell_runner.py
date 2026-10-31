import subprocess
import json
from pathlib import Path

from lehaneos.core.logging_config import configure_logging
from lehaneos.core.exceptions.base import PowershellError

logger = configure_logging()


class PowerShellRunner:

    def run(self, script: Path, *args):
        """
        Execute a PowerShell script and parse
        its JSON response.

        Args:
            script: Full path of the PowerShell script.
            *args: Arguments passed to the script.

        Returns:
            dict: Parsed JSON response.

        Raises:
            PowerShellError: If the script execution
            fails or if the returned JSON is invalid.
        """

        script_name= Path(script).stem

        logger.info(f"Launching Powershell script")
        logger.info(f"Script: {script}")
        logger.info(f"Arguments: {args}")

        pwsh_command = subprocess.run(
            [
                "powershell.exe",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                script,
                *args
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