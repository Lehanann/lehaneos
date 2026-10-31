from pydantic import BaseModel, Field

class Company(BaseModel):
    """Represents a company"""
    name: str = Field(..., description="Company name")
    street: str = Field(..., description="Company street")
    city: str = Field(..., description="Company city")
    country: str = Field(..., description="Company country")
    domain: str = Field(..., description="Company domain")
    email_domain: str = Field(..., description="Company email domain")