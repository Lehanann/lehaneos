from pydantic import BaseModel, Field

class Service(BaseModel):
    display_name: str = Field(..., description="Service display name")
    department: str  = Field(..., description="Service department")