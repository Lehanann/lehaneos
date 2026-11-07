import re

from lehaneos.core.sanitizers.string_sanitizer import StringSanitizer


class AccountIdentityBuilder:
    """
    Builds identity-related attributes for a user account.
    """

    def build_username(self, first_name: str, last_name: str) -> str:
        """
        Builds a username using the initials of the first name and the full last name.

        Returns :
            Sanitized username built from the initials of the first name and the full last name.
        """
        initial_first_name = "".join(re.findall(r"\b\w", first_name)).lower()
        username = initial_first_name + last_name.replace(" ", "").lower()

        return StringSanitizer.sanitize_username(username)

    def build_display_name(self, first_name: str, last_name: str) -> str:
        """
        Builds a display name using the first and last name.

        Returns:
            Display name built with first name and last name capitalized.
        """
        return first_name.title() + " " + last_name.title()

    def build_email(self, email_domain: str, first_name: str, last_name: str) -> str:
        """
        Builds an email address using username and email domain name.

        Args:
            email_domain (str): Email domain name.
            first_name (str): First name.
            last_name (str): Last name.

        Returns:
             Email address built from the username and the email domain.
        """
        return self.build_username(first_name, last_name) + "@" + email_domain

    def build_upn(self, domain_name: str, first_name: str, last_name: str) -> str:
        """
        Builds a User Principal Name(UPN) using username and active directory domain.

        Args:
            domain_name (str): Active directory domain name.
            first_name (str): First name.
            last_name (str): Last name.

        Returns:
             User Principale Name built from the username and the active directory domain.
        """
        return self.build_username(first_name, last_name) + "@" + domain_name
