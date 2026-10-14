from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class ADUser(BaseModel):
    """
    Represents an Active Directory user.
    """
    username: str = Field(..., description="Active directory username")
    email: EmailStr | None = Field(None, description="User email address")
    first_name: str | None = Field(None, description="User first name")
    last_name: str | None = Field(None, description="User last name")
    phone_number: str | None = Field(None, description="User phone number")
    mobile_phone: str | None = Field(None, description="User Mobile phone")
    display_name: str | None = Field(None, description="User display name")
    distinguished_name: str = Field(..., description="User distinguished name")
    department: str | None = Field(None, description="User Department")
    account_expires: datetime | None = Field(None, description="Account expiration date")
    user_principal_name: str = Field(..., description="User principal name")
    proxy_addresses: list[str] = Field(default_factory=list, description="Email addresses list")
    groups: list[str] = Field(default_factory=list, description="Group names list")
    groups_dn: list[str] = Field(default_factory=list, description="Group distinguished names list")
    description: str | None = Field(None, description="User Description")
    title: str | None = Field(None, description="User title")
    company: str | None = Field(None, description="User company")
    street_address: str | None = Field(None, description="User street address")
    city: str | None = Field(None, description="User city")
    country: str | None = Field(None, description="User country")
