import json
from pathlib import Path
import logging
from lehaneos.core.exceptions.base import PowershellError
from lehaneos.core.ssh.ssh_manager import SSHManager
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PowerShellRunner:

    def __init__(self, ssh_client: SSHManager):
        """
        Initialize a new PowerShell runner.

        Args:
            ssh_client: SSH client used to execute remote commands.
        """
        self.ssh_client = ssh_client

    def run(self, script: Path, parameters: BaseModel):
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

        script_name = Path(script).stem
        payload = json.dumps(parameters.model_dump())

        logger.info("Launching Powershell script")
        logger.info("Script: %s", script)
        logger.info("Arguments: %s", parameters)

        pwsh_command = self._build_command(script)
        self.ssh_client.connect()
        try:
            result = self.ssh_client.execute_command(command=pwsh_command, stdin_data=payload)
        finally:
            self.ssh_client.disconnect()

        logger.info("Return code: %s", result.exit_status)

        if result.stderr:
            logger.error("Stderr: %s", result.stderr)

        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {result.stdout}")
            raise PowershellError("Invalid JSON returned by Powershell") from e

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


    def _build_command(self,script: Path) -> str:
        """
        Build the PowerShell execution command.

        Args:
            script: Remote PowerShell script path.

        Returns:
            str: Complete PowerShell command.
        """
        command = (
            f'pwsh.exe '
            f'-ExecutionPolicy Bypass '
            f'-File "{script}" '
        )
        return command
