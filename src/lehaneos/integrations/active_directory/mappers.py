from ldap3 import Entry

from lehaneos.integrations.active_directory.schemas.ad_group import ADGroup
from lehaneos.integrations.active_directory.schemas.ad_user import ADUser

class ADUserMapper:

    @staticmethod
    def entry_to_user(entry: Entry) -> ADUser:
        """
        Convert an LDAP entry into an ADUser object.

        Args:
            entry: LDAP user entry returned by ldap3.

        Returns:
            A populated ADUser instance.
        """
        data = entry.entry_attributes_as_dict
        return ADUser(
            username=data['sAMAccountName'][0],
            email=data.get("mail", [None])[0],
            first_name=data.get('givenName', [None])[0],
            last_name=data.get('sn', [None])[0],
            phone_number=data.get('telephoneNumber', [None])[0],
            mobile_phone=data.get('mobile', [None])[0],
            display_name=data.get('displayName', [None])[0],
            distinguished_name=data['distinguishedName'][0],
            department=data.get('department', [None])[0],
            account_expires=data.get('accountExpires', [None])[0],
            user_principal_name=data['userPrincipalName'][0],
            proxy_addresses=data.get('proxyAddresses', []),
            groups_dn=data.get('memberOf', []),
            groups=[dn.split(",")[0].replace("CN=","") for dn in data.get('memberOf', [])],
            description=data.get('description', [None])[0],
            title=data.get('title', [None])[0],
            company=data.get('company', [None])[0],
            street_address=data.get('streetAddress', [None])[0],
            city=data.get("l", [None])[0],
            country=data.get("c", [None])[0],
        )

class ADGroupMapper:

    @staticmethod
    def entry_to_group(entry: Entry) -> ADGroup:
        """
        Convert an LDAP entry into an ADGroup object.

        Args:
            entry: LDAP group entry returned by ldap3.

        Returns:
            A populated ADGroup instance.
        """
        data = entry.entry_attributes_as_dict
        return ADGroup(
            name=data.get('name', [None])[0],
            distinguished_name=data.get('distinguishedName', [None])[0],
            members_dn=data.get('member', []),
            members=[dn.split(",")[0].replace("CN=","") for dn in data.get('member', [])],
            description=data.get('description', [None])[0],
            created_at=data.get('whenCreated', [None])[0],
            updated_at=data.get('whenChanged', [None])[0],
        )