import secrets
import string


class PasswordGenerator:
    @staticmethod
    def generate(size=14) -> str:
        """
        Generates a secure temporary password.

        Args:
            size: Password length.

        Returns:
            Random password containing uppercase letters, lowercase
            letters, digits and special characters.

        Raises:
            ValueError: If the password length is less than 14 characters.
        """
        if size < 14:
            raise ValueError("Password must be at least 14 characters.")
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_characters = "!#&@/%$"

        all_characters = (
            uppercase_letters + lowercase_letters + digits + special_characters
        )

        password = [
            secrets.choice(uppercase_letters),
            secrets.choice(lowercase_letters),
            secrets.choice(digits),
            secrets.choice(special_characters),
        ]

        for _ in range(size - len(password)):
            password.append(secrets.choice(all_characters))

        secrets.SystemRandom().shuffle(password)
        return "".join(password)
