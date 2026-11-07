import paramiko
from paramiko.ssh_exception import NoValidConnectionsError, PasswordRequiredException

from lehaneos.core.ssh.exceptions import (
    SSHConnectionError,
    SSHEncodingError,
    SSHError,
    SSHNotConnectedError,
    SSHPrivateKeyError,
    SSHTimeoutError,
)
from lehaneos.core.ssh.ssh_result import SSHResult


class SSHManager:
    """
    Manage SSH connections and remote command execution.

    This class is responsible for establishing SSH connections,
    executing remote commands and returning standardized
    SSHResult objects.

    It wraps Paramiko and exposes LehanEOS-specific exceptions.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str | None = None,
        key_filename: str | None = None,
        port: int = 22,
        encoding: str = "utf-8",
    ) -> None:
        """
        Initialize a new SSH manager.

        Args:
            host: Remote host address.
            username: SSH username.
            password: SSH password.
            key_filename: Path to the private key.
            port: SSH service port.
            encoding: Remote output encoding.
        """
        self.host = host
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.encoding = encoding
        self._client: paramiko.SSHClient | None = None

    def connect(self) -> None:
        """
        Establish an SSH connection.

        If a connection already exists, the method returns
        without creating a new one.

        Raises:
            SSHTimeoutError: Raised when the connection times out.
            SSHConnectionError: Raised when the host cannot be reached.
            SSHPrivateKeyError: Raised when the private key cannot be loaded.
            SSHError: Raised for any unexpected SSH error.
        """
        if self._client is not None:
            return
        try:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename,
                timeout=10,
            )
        except TimeoutError as e:
            self._client = None
            raise SSHTimeoutError() from e

        except NoValidConnectionsError as e:
            self._client = None
            raise SSHConnectionError() from e

        except PasswordRequiredException as e:
            self._client = None
            raise SSHPrivateKeyError() from e

        except Exception as e:
            self._client = None
            raise SSHError() from e

    def execute_command(self, command: str, stdin_data: str | None = None) -> SSHResult:
        """
        Execute a remote command through SSH.

        Args:
            command: Command to execute remotely.
            stdin_data: Optional data sent to the command standard input.

        Returns:
            SSHResult: Command execution result.

        Raises:
            SSHNotConnectedError: Raised when no SSH connection is available.
            SSHEncodingError: Raised when command output cannot be decoded.
        """
        if self._client is None:
            raise SSHNotConnectedError()

        try:
            stdin, stdout, stderr = self._client.exec_command(command)

            if stdin_data:
                stdin.write(stdin_data)
                stdin.flush()
                stdin.channel.shutdown_write()

            stdout_bytes = stdout.read()
            stderr_bytes = stderr.read()
            exit_status = stdout.channel.recv_exit_status()

            return SSHResult(
                stdout=stdout_bytes.decode(self.encoding),
                stderr=stderr_bytes.decode(self.encoding),
                exit_status=exit_status,
            )

        except UnicodeDecodeError as e:
            raise SSHEncodingError() from e

    def disconnect(self) -> None:
        """
        Close the active SSH connection.

        If no connection exists, nothing happens.
        """
        if self._client:
            self._client.close()
            self._client = None
