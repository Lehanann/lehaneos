import pytest
from lehaneos.core.security.password_generator import PasswordGenerator

def test_generator() -> None:
    password = PasswordGenerator.generate()

    assert len(password) >= 14

def test_generate_password_too_short():
    with pytest.raises(ValueError):
        PasswordGenerator.generate(10)
