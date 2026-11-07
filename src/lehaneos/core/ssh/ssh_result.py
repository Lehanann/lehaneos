from pydantic import BaseModel, Field


class SSHResult(BaseModel):
    """
    Represents an SSH result.
    """

    stdout: str = Field(..., description="The stdout of the command")
    stderr: str = Field(..., description="The stderr of the command")
    exit_status: int = Field(..., description="The exit status of the command")
