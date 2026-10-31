from pydantic import BaseModel, Field

class Job(BaseModel):
    """Represents a job"""
    title: str = Field(..., description="Job title")
    organization_unit: str = Field(..., description="Organization unit")
    groups: list[str] = Field(default_factory=list, description="Groups")