from pydantic import BaseModel, Field

class UserDeletion(BaseModel):
    """
    Represent a user deletion.
    """
    username: str = Field(..., description="Username of the user to delete")
