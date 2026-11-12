from pydantic import BaseModel, Field

class UserIdentity(BaseModel):
    """
    Represent a user deletion.
    """
    username: str = Field(..., description="Username of the user to delete")
