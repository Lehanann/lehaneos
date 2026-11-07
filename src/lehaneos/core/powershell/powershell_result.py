from typing import Any
from pydantic import BaseModel,  Field
from lehaneos.core.powershell.powershell_status import PowerShellStatus

class PowerShellResult(BaseModel):
    """
    Standard response returned by PowerShell scripts.
    """
    code: str = Field(..., description="Powershell code.")
    status: PowerShellStatus = Field(..., description="Powershell status")
    message: str = Field(..., description="Powershell message")
    data: dict[str, Any] = Field(..., description="Powershell data")