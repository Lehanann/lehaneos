from lehaneos.settings.settings import settings
from ldap3 import Server, Connection, ALL, Entry

class ActiveDirectoryClient:

    def __init__(self) -> None:
        self.connection: Connection | None = None
        self.server: Server = Server(settings.ad_server, get_info=ALL)
        self.ad_username: str = settings.ad_username

    def connect(self) -> None:
        if self.connection is None:
            self.connection = Connection(self.server,user=self.ad_username, password=settings.ad_password.get_secret_value())
            if self.connection.bind():
                print("Connected")
            else:
                print("Failed to connect")
        else:
            print("Already connected.")

    def search(self,search_base: str, search_filter: str, attributes: list[str] | None=None)->list[Entry]:
        if self.connection is None:
            return []
        if attributes is None:
            attributes = ["*"]

        self.connection.search(search_base=search_base, search_filter=search_filter,attributes=attributes)
        return self.connection.entries


    def search_user(self, username: str) -> Entry | None:
        entries = self.search(settings.users_dn, f'(sAMAccountName={username})', attributes=[
            "displayName",
            "mail",
            "memberOf",
        ])

        return entries[0] if entries else None

    def search_group(self, group_name: str) -> Entry | None:
        entries = self.search(settings.groups_dn, f'(&(objectClass=group)(cn={group_name}))', attributes=[
            "cn",
            "name",
            "description",
            "member",
        ])
        return entries[0] if entries else None

    def user_exists(self, username: str) -> bool:
        if self.search_user(username) is None:
            return False
        else:
            return True

    def group_exists(self, group_name: str) -> bool:
        if self.search_group(group_name) is None:
            return False
        else:
            return True

    def disconnect(self):
        self.connection.unbind()