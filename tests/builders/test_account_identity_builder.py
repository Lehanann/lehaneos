from lehaneos.integrations.active_directory.provisioning.builders.account_identity_builder import (
    AccountIdentityBuilder
)

def test_build_username():
    builder = AccountIdentityBuilder()

    username = builder.build_username(
        first_name="Jean-Pierre",
        last_name="Dupont"
    )

    assert username == "jpdupont"

def test_build_username_with_accents():
    builder = AccountIdentityBuilder()

    username = builder.build_username(
        first_name="Jérôme",
        last_name=" Millésimé"
    )
    assert username == "jmillesime"

def test_build_display_name():
    builder = AccountIdentityBuilder()
    display_name = builder.build_display_name(
        first_name="Jean-Pierre",
        last_name="Dupont"
    )
    assert display_name == "Jean-Pierre Dupont"

def test_build_display_name_with_accent():
    builder = AccountIdentityBuilder()
    display_name = builder.build_display_name(
        first_name="Jérôme",
        last_name="Millésimé"
    )
    assert display_name == "Jérôme Millésimé"

def test_build_email():
    builder = AccountIdentityBuilder()
    email = builder.build_email("lehaneos.lan", "Jean-Pierre", "Dupont")
    assert email == "jpdupont@lehaneos.lan"


def test_build_upn():
    builder = AccountIdentityBuilder()
    upn = builder.build_upn("lehaneos.lan", "Jean-Pierre", "Dupont")
    assert upn == "jpdupont@lehaneos.lan"