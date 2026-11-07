class SSHError(Exception):
    """
    Base exception for SSH operations.
    """


class SSHConnectionError(SSHError):
    """
    Raised when the SSH connection cannot be established.
    """


class SSHPrivateKeyError(SSHError):
    """
    Raised when the SSH private key cannot be loaded or used.
    """


class SSHAuthenticationError(SSHError):
    """
    Raised when SSH authentication fails.
    """


class SSHTimeoutError(SSHError):
    """
    Raised when an SSH connection times out.
    """


class SSHNotConnectedError(SSHError):
    """
    Raised when attempting to execute a command without an active SSH connection.
    """


class SSHEncodingError(SSHError):
    """Raised when SSH output cannot be decoded."""
