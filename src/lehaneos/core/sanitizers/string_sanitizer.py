import unicodedata

class StringSanitizer:

    @staticmethod
    def sanitize_username(username: str) -> str:
        """
        Removes diacritical marks from a username.
        Args:
             username(str): Username to sanitize
        Returns:
            Sanitized username without accented characters.
        """
        new_username = unicodedata.normalize("NFD", username)
        return "".join(c for c in new_username if unicodedata.category(c) != 'Mn')