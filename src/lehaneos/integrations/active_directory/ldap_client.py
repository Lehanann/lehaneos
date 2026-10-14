import logging
from lehaneos.settings.settings import settings
from ldap3 import Server, Connection, ALL, Entry
from lehaneos.integrations.active_directory.exceptions import ActiveDirectoryConnectionError, ActiveDirectorySearchError
from lehaneos.integrations.active_directory.schemas.ad_user import ADUser
from lehaneos.integrations.active_directory.schemas.ad_group import ADGroup
from lehaneos.integrations.active_directory.mappers import ADUserMapper, ADGroupMapper

logger = logging.getLogger(__name__)

class ActiveDirectoryClient:

    def __init__(self) -> None:
        self.connection: Connection | None = None
        self.server: Server = Server(settings.ad_server, get_info=ALL)
        self.ad_username: str = settings.ad_username

    def connect(self) -> None:
        if self.connection is None:
            self.connection = Connection(self.server,user=self.ad_username, password=settings.ad_password.get_secret_value())
            if not self.connection.bind():
                logger.error("Unable to connect to LDAP Server")
                raise ActiveDirectoryConnectionError("Unable to connect to LDAP Server")
            logger.info("Connected to LDAP Server")
        else:
            logger.info("LDAP Server already connected")

    def search(self,search_base: str, search_filter: str, attributes: list[str] | None=None)->list[Entry]:
        if self.connection is None:
            logger.error("LDAP search attempted without an active connection")
            raise ActiveDirectorySearchError("LDAP Server not established")

        if attributes is None:
            attributes = ["*"]

        self.connection.search(search_base=search_base, search_filter=search_filter,attributes=attributes)
        return self.connection.entries

    def search_user(self, username: str) -> ADUser | None:
        entries = self.search(settings.users_dn, f'(sAMAccountName={username})')
        if not entries:
            return None
        return ADUserMapper.entry_to_user(entries[0])

    def search_group(self, group_name: str) -> ADGroup | None:
        entries = self.search(settings.groups_dn, f'(&(objectClass=group)(cn={group_name}))')
        if not entries:
            return None
        return ADGroupMapper.entry_to_group(entries[0])

    def user_exists(self, username: str) -> bool:
       return self.search_user(username) is not None

    def group_exists(self, group_name: str) -> bool:
        return self.search_group(group_name) is not None

    def get_user_groups(self, username: str) -> list[str] | None:
        user = self.search_user(username)
        if not user:
            return None
        return user.groups

    def get_group_members(self, group_name: str) -> list[str] | None:
        group = self.search_group(group_name)
        if not group:
            return None
        return group.members

    def disconnect(self) -> None:
        if self.connection is None:
            logger.error("Not connected to LDAP Server")
            raise ActiveDirectoryConnectionError("Not connected to LDAP Server")
        self.connection.unbind()
        self.connection = None
        logger.info("Disconnected from LDAP Server")

