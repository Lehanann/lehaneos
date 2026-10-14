import logging
from lehaneos.settings.settings import settings
from ldap3 import Server, Connection, ALL, Entry
from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryConnectionError,
    ActiveDirectorySearchError,
    ActiveDirectoryGroupNotFoundError,
    ActiveDirectoryUserNotFoundError
)
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
        """
        Establish a connection to the LDAP server.

        Raises:
            ActiveDirectoryConnectionError:
                If the connection cannot be established.
        """
        if self.connection is None:
            self.connection = Connection(self.server,user=self.ad_username, password=settings.ad_password.get_secret_value())
            if not self.connection.bind():
                logger.error("Unable to connect to LDAP Server")
                raise ActiveDirectoryConnectionError("Unable to connect to LDAP Server")
            logger.info("Connected to LDAP Server")
        else:
            logger.info("LDAP Server already connected")

    def search(self,search_base: str, search_filter: str, attributes: list[str] | None = None) -> list[Entry]:
        """
        Perform an LDAP search operation.

        Args:
            search_base: Distinguished name used as the search base.
            search_filter: LDAP search filter.
            attributes: Attributes to retrieve. Defaults to all attributes.

        Returns:
            A list of LDAP entries matching the search criteria.

        Raises:
            ActiveDirectorySearchError:
                If no LDAP connection is established.
        """
        if self.connection is None:
            logger.error("LDAP search attempted without an active connection")
            raise ActiveDirectorySearchError("LDAP Server not established")
        if attributes is None:
            attributes = ["*"]
        self.connection.search(search_base=search_base, search_filter=search_filter,attributes=attributes)
        return self.connection.entries

    def search_user(self, username: str) -> ADUser | None:
        """
        Search for a user in Active Directory.

        Args:
            username: User logon name (sAMAccountName).

        Returns:
            The matching ADUser object if found, otherwise None.
        """
        entries = self.search(settings.users_dn, f'(sAMAccountName={username})')
        if not entries:
            return None
        return ADUserMapper.entry_to_user(entries[0])

    def search_group(self, group_name: str) -> ADGroup | None:
        """
        Search for a group in Active Directory.

        Args:
            group_name: Group common name.

        Returns:
            The matching ADGroup object if found otherwise None.
        """
        entries = self.search(settings.groups_dn, f'(&(objectClass=group)(cn={group_name}))')
        if not entries:
            return None
        return ADGroupMapper.entry_to_group(entries[0])

    def user_exists(self, username: str) -> bool:
        """
        Check whether a user exists.

        Args:
            username: User logon name (sAMAccountName).

        Returns:
            True if the user exists, otherwise False.
        """
        return self.search_user(username) is not None

    def group_exists(self, group_name: str) -> bool:
        """
        Check whether a group exists.

        Args:
            group_name: Group common name.

        Returns:
            True if the group exists, otherwise False.
        """
        return self.search_group(group_name) is not None

    def get_user_groups(self, username: str) -> list[str]:
        """
        Retrieve all groups assigned to a user.

        Args:
            username: User logon name.

        Returns:
            A list containing the names of all groups the user belongs to.

        Raises:
            ActiveDirectoryUserNotFoundError:
                If the specified user does not exist.
        """
        user = self.search_user(username)
        if user is None:
            raise ActiveDirectoryUserNotFoundError(f"User '{username}' not found.")
        return user.groups

    def get_group_members(self, group_name: str) -> list[str]:
        """
        Retrieve all members of a group.

        Args:
            group_name: Group common name.

        Returns:
            A list containing the names of the group's members.

        Raises:
            ActiveDirectoryGroupNotFoundError:
                If the specified group does not exist.
        """
        group = self.search_group(group_name)
        if group is None:
            raise ActiveDirectoryGroupNotFoundError(f"Group '{group_name}' not found.")
        return group.members

    def is_member_of(self, username: str, group_name: str) -> bool:
        """
        Check whether a user belongs to a group.

        Args:
            username: User logon name (sAMAccountName).
            group_name: Group common name.

        Returns:
            True if the user belongs to the group, otherwise False.

        Raises:
            ActiveDirectoryUserNotFoundError:
                If the specified user does not exist.
            ActiveDirectoryGroupNotFoundError:
                If the specified group does not exist.
        """
        user = self.search_user(username)
        if user is None:
            raise ActiveDirectoryUserNotFoundError(f"User '{username}' not found.")
        group = self.search_group(group_name)
        if group is None:
            raise ActiveDirectoryGroupNotFoundError(f"Group '{group_name}' not found.")
        return user.distinguished_name in group.members_dn

    def disconnect(self) -> None:
        """
        Disconnect an established connection to the LDAP server.

        Raises:
            ActiveDirectoryConnectionError:
                If no connection is established.
        """
        if self.connection is None:
            logger.error("Not connected to LDAP Server")
            raise ActiveDirectoryConnectionError("Not connected to LDAP Server")
        self.connection.unbind()
        self.connection = None
        logger.info("Disconnected from LDAP Server")

