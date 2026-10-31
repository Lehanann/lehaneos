from pydantic import BaseModel, Field, EmailStr


class UserAccountProvisioning(BaseModel):
    """
    Represents the data required to provision an Active Directory user account.
    """
    username: str = Field(..., description="Active directory username")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    display_name: str = Field(..., description="User display name")
    organization_unit_dn: str = Field(..., description="Target organization unit distinguished name")
    temporary_password: str = Field(..., description="Temporary user password")
    user_principal_name: str = Field(..., description="User principal name")
    proxy_addresses: list[str] = Field(default_factory=list, description="Email addresses list")
    groups_dn: list[str] = Field(default_factory=list, description="Group distinguished names list")
    title: str = Field(..., description="User title")
    company: str = Field(..., description="User company")
    street_address: str = Field(..., description="User street address")
    city: str = Field(..., description="User city")
    country: str = Field(..., description="User country")