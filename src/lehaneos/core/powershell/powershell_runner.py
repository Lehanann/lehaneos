import subprocess
import json
from pathlib import Path
import logging
from lehaneos.core.exceptions.base import PowershellError
from lehaneos.core.ssh.ssh_manager import SSHManager
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PowerShellRunner:

    def __init__(self, ssh_client: SSHManager):
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

        logger.info(f"Launching Powershell script")
        logger.info(f"Script: {script}")
        logger.info(f"Arguments: {parameters}")

        pwsh_command = self._build_command(script)
        self.ssh_client.connect()
        try:
            result = self.ssh_client.execute_command(command=pwsh_command, stdin_data=payload)
            print("RESULT STDOUT")
            print(repr(result.stdout))

            print("RESULT STDERR")
            print(repr(result.stderr))
        finally:
            self.ssh_client.disconnect()

        return json.loads(result.stdout)
        """    
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
   
        logger.info(f"Return code: {result.exit_status}")

        if result.stderr:
            logger.error(f"Stderr: {result.stderr}")

        try:
            print("RETURN CODE:", result.exit_status)
            print("STDOUT:", repr(result.stdout))
            print("STDERR:", repr(result.stderr))
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {result.stdout}")
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
        return response   """
    """
    def _build_arguments(self, parameters: dict) -> list[str]:
        build_parameters = []
        for key, value in parameters.items():
            if isinstance(value, list):
                values = ",".join(f'"{item}"' for item in value)
                build_parameters.append(f'-{key} {values}')
            else:
                build_parameters.append(f'-{key} "{value}"')

        return build_parameters
    """
    def _build_command(self,script: Path) -> str:
        command = (
            f'pwsh.exe '
            f'-ExecutionPolicy Bypass '
            f'-File "{script}" '
        )
        print(command)
        return command
