from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserAccountProvisioning(BaseModel):
    """
    Represents the data required to provision an Active Directory user account.
    """
    username: str = Field(..., description="Active directory username",alias="Username")
    email: EmailStr = Field(..., description="User email address",alias="Email")
    first_name: str = Field(..., description="User first name",alias="FirstName")
    last_name: str = Field(..., description="User last name",alias="LastName")
    display_name: str = Field(..., description="User display name",alias="DisplayName")
    organization_unit_dn: str = Field(..., description="Target organization unit distinguished name",alias="OrganizationUnitDN")
    temporary_password: str = Field(..., description="Temporary user password",alias="TemporaryPassword")
    user_principal_name: str = Field(..., description="User principal name",alias="UserPrincipalName")
    proxy_addresses: list[str] = Field(default_factory=list, description="Email addresses list",alias="ProxyAddresses")
    groups_dn: list[str] = Field(default_factory=list, description="Group distinguished names list",alias="GroupsDN")
    title: str = Field(..., description="User title",alias="Title")
    company: str = Field(..., description="User company",alias="Company")
    street_address: str = Field(..., description="User street address",alias="StreetAddress")
    city: str = Field(..., description="User city",alias="City")
    country: str = Field(..., description="User country",alias="Country")

    model_config = ConfigDict(populate_by_name=True)