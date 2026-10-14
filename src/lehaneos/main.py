from lehaneos.core.logging_config import configure_logging
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient

configure_logging()

ad = ActiveDirectoryClient()
ad.connect()
user = ad.search_user("jdupont")
print("user",user)
print("####")
print("GROUP", ad.search_group("GRP_ADM_LEHANEOS"))
print("####")
print("jdupont exists:",ad.user_exists("jdupont"))
print("group GRP_ADM_LEHANEOS exists:",ad.group_exists("GRP_ADM_LEHANEOS"))
print("###")
print("USER GROUP", ad.get_user_groups("jdupont") )
print("###")
print("MEMBERS OF GRP_LEHANEOS_LDAP \n",ad.get_group_members("GRP_LEHANEOS_LDAP"))
print("###")
print(ad.is_member_of("jdupont","GRP_ADM_LEHANEOS"))

ad.disconnect()