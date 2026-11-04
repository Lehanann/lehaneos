
class SSHError(Exception):
    """
    Base exception for SSH operations.
    """
    pass

class SSHConnectionError(SSHError):
    """
    Raised when the SSH connection cannot be established.
    """
    pass

class SSHPrivateKeyError(SSHError):
    """
    Raised when the SSH private key cannot be loaded or used.
    """
    pass

class SSHAuthenticationError(SSHError):
    """
    Raised when SSH authentication fails.
    """
    pass

class SSHTimeoutError(SSHError):
    """
    Raised when an SSH connection times out.
    """
    pass

class SSHNotConnectedError(SSHError):
    """
    Raised when attempting to execute a command without an active SSH connection.
    """
    pass

class SSHEncodingError(SSHError):
    """Raised when SSH output cannot be decoded."""
    pass