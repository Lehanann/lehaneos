from pydantic import BaseModel, Field

class UserIdentity(BaseModel):
    """
    Represent a user identity used by user lifecycle operations.
    """
    username: str = Field(..., description="Username of the user to delete")

class UserResetPassword(UserIdentity):
    """
    Represent a password reset request.
    """
    new_password: str = Field(..., description="New temporary password")