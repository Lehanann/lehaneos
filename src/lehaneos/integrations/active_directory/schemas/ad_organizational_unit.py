from datetime import datetime

from pydantic import BaseModel, Field


class ADOrganizationalUnit(BaseModel):
    """
    Represents an Active Directory organizational unit.
    """

    distinguished_name: str = Field(..., description="Distinguished name of organizational unit.")
    organizational_unit_name: str = Field(..., description="Organizational unit name.")
    created_at: datetime | None = Field(None, description="Group creation date ")
    updated_at: datetime | None = Field(None, description="Group last update date ")