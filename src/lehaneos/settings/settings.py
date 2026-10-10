from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ==================================================================
    # Active Directory
    # ==================================================================
    ad_server: str = Field(default="DC01.domain.local")
    ad_domain: str = Field(default="domain.local")
    ad_username: str = Field(default="")
    ad_password: SecretStr = Field(default=SecretStr(""))
    ad_base_dn: str = Field(default="DC=DOMAIN,DC=LOCAL")
    ad_users_ou: str = Field(default="OU=Users")
    ad_groups_ou: str = Field (default="OU=Groups")
    ad_port: int = Field(default=389)

    @property
    def users_dn(self):
        return f"{self.ad_users_ou},{self.ad_base_dn}"
    @property
    def groups_dn(self):
        return f"{self.ad_groups_ou},{self.ad_base_dn}"

settings = Settings()