from pydantic import BaseModel, Field


class OrganizationUnit(BaseModel):
    """Represents an organization unit"""

    display_name: str = Field(..., description="Organization name")
    ou_name: str = Field(..., description="Organization OU name")
