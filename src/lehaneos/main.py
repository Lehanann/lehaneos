from lehaneos.settings.settings import settings
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient


ad = ActiveDirectoryClient()
ad.connect()
entities = ad.search(settings.ad_base_dn, '(sAMAccountName=ygrondin-adm)', ["*"])
print(entities)

user = ad.search_user("ygrondin-adm")
print("user",user)

group = ad.search_group("GRP_LEHANEOS_LDAP")
print(group)

print(ad.user_exists("ygrondin-adm"))
print(ad.group_exists("GRP_LEHANEOS_LDAP"))