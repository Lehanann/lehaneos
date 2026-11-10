from pydantic import BaseModel, Field

class Department(BaseModel):
    """Represents a department"""

    display_name: str = Field(..., description="Department display name")