from pydantic import BaseModel, Field
from datetime import datetime

class ADGroup(BaseModel):
    name: str = Field(..., description="Active directory group name")
    distinguished_name: str = Field(..., description="Group distinguished name")
    members_dn: list['str'] = Field(default_factory=list, description="Group member list")
    members: list['str'] = Field(default_factory=list, description="Group member list DN")
    description: str | None = Field(None, description="Group description")
    created_at: datetime | None = Field(None, description="Group creation date ")
    updated_at: datetime | None = Field(None, description="Group last update date ")

