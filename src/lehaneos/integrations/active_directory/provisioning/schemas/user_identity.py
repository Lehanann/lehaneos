from pydantic import BaseModel, Field


class UserIdentityBase(BaseModel):
    username: str = Field(..., description="Username of the user to delete")
    display_name: str | None = Field(None, description="Display name of the user to delete")

class UserIdentityLifecycle(UserIdentityBase):
    """
    Represent a user identity used by user lifecycle operations.
    """
    distinguished_name: str = Field(..., description="Distinguished name of the user to delete")
    target_ou_dn: str = Field(..., description="Target Organization Unit DN")

class UserResetPassword(UserIdentityBase):
    """
    Represent a password reset request.
    """
    new_password: str = Field(..., description="New temporary password")