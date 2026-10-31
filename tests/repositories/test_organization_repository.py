from lehaneos.integrations.active_directory.provisioning.repositories.organisation_repository import OrganizationRepository

def test_get_company():
    orga_repo = OrganizationRepository()

    company = orga_repo.get_company()
    assert company is not None
    assert company.name == "LehanEOS"
    assert company.street == "1 rue de la république"
    assert company.city =="Lyon"
    assert company.country == "FR"
    assert company.domain == "lehaneos.lan"
    assert company.email_domain == "lehaneos.lan"

def test_get_ou():
    orga_repo = OrganizationRepository()

    ou = orga_repo.get_organization_unit("admins")
    assert ou is not None
    assert ou.display_name == "Admins"
    assert ou.ou_name == "Admins"