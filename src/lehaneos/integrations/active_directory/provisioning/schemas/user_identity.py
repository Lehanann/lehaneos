from pydantic import BaseModel, Field


class UserIdentityBase(BaseModel):
    """
    Represent a minimal user identity.
    """
    username: str = Field(..., description="Active Directory username")
    display_name: str | None = Field(None, description="Display name of the user")

class UserIdentity(UserIdentityBase):
    """
    represents  a user identity used with distinguished name.
    """
    distinguished_name: str = Field(..., description="Distinguished name of the user")


class UserMove(UserIdentity):
    """
    Represent a user identity used by user lifecycle with enable and disable operations.
    """
    target_ou_dn: str = Field(..., description="Target organizational unit distinguished name")

class UserResetPassword(UserIdentityBase):
    """
    Represent a password reset request.
    """
    new_password: str = Field(..., description="New temporary password")