from pytest_mock import MockerFixture
import pytest
from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserAlreadyExistsError,
    ActiveDirectoryJobNotFoundError,
    ActiveDirectoryCompanyNotFoundError,
    ActiveDirectoryOrganizationUnitNotFoundError, ActiveDirectoryGroupNotFoundError,
)
from lehaneos.integrations.active_directory.provisioning.services.user_provisioning_service import (
    UserProvisioningService
)

def test_provision_username_already_exists(mocker) -> None:
    ad_client = mocker.Mock()
    ad_client.user_exists.return_value = True

    service = UserProvisioningService(
        active_directory_client=ad_client,
        job_repository=mocker.Mock(),
        organization_repository=mocker.Mock(),
        account_identity_builder=mocker.Mock(),
    )

    with pytest.raises(ActiveDirectoryUserAlreadyExistsError):
        service.provision(
            "Elisa",
            "Durand",
            "system_administrator"
        )

def test_provision_success(mocker: MockerFixture) -> None:
    ad_client = mocker.Mock()
    ad_client.user_exists.return_value = False

    job = mocker.Mock()
    job.title = "Administrateur systèmes"
    job.organization_unit = "admins"
    job.groups = ["GRP_DEPT_IT"]

    job_repository = mocker.Mock()
    job_repository.get_job.return_value = job

    company = mocker.Mock()
    company.name = "LehanEOS"
    company.street = "1 rue de la république"
    company.city = "Lyon"
    company.country = "FR"
    company.domain = "lehaneos.lan"
    company.email_domain = "lehaneos.lan"

    organization_repository = mocker.Mock()
    organization_repository.get_company.return_value = company

    organization_unit = mocker.Mock()
    organization_unit.ou_name = "Admins"

    organization_repository.get_organization_unit.return_value = organization_unit

    ad_group = mocker.Mock()
    ad_group.distinguished_name = "CN=GRP_DEPT_IT,OU=Groups,DC=lehaneos,DC=lan"

    ad_client.search_group.return_value = ad_group

    identity_builder = mocker.Mock()
    identity_builder.build_username.return_value = "edurand"
    identity_builder.build_display_name.return_value = "Elisa Durand"
    identity_builder.build_email.return_value = "edurand@lehaneos.lan"
    identity_builder.build_upn.return_value = "edurand@lehaneos.lan"

    mocker.patch(
        "lehaneos.core.security.password_generator.PasswordGenerator.generate",
        return_value="Password123!"
    )

    service = UserProvisioningService(
        active_directory_client=ad_client,
        job_repository=job_repository,
        organization_repository=organization_repository,
        account_identity_builder=identity_builder,
    )

    result = service.provision(
        first_name="Elisa",
        last_name="Durand",
        job_name="system_administrator",
    )


    assert result.username == "edurand"
    assert result.email == "edurand@lehaneos.lan"
    assert result.display_name == "Elisa Durand"
    assert result.company == "LehanEOS"
    assert result.title == "Administrateur systèmes"
    assert result.temporary_password == "Password123!"
    ad_client.user_exists.assert_called_once_with("edurand")
    job_repository.get_job.assert_called_once_with("system_administrator")

def test_provision_job_not_found(mocker ) -> None:
    ad_client = mocker.Mock()
    ad_client.user_exists.return_value = False

    job_repository = mocker.Mock()
    job_repository.get_job.return_value = None

    identity_builder = mocker.Mock()
    identity_builder.build_username.return_value = "edurand"
    identity_builder.build_display_name.return_value = "Elisa Durand"
    identity_builder.build_email.return_value = "edurand@lehaneos.lan"
    identity_builder.build_upn.return_value = "edurand@lehaneos.lan"

    mocker.patch(
        "lehaneos.core.security.password_generator.PasswordGenerator.generate",
        return_value="Password123!"
    )

    service = UserProvisioningService(
        active_directory_client=ad_client,
        job_repository=job_repository,
        organization_repository=mocker.Mock(),
        account_identity_builder=identity_builder,
    )
    with pytest.raises(ActiveDirectoryJobNotFoundError):
        service.provision(
            "Elisa",
            "Durand",
            "system_administrator"
        )

def test_provision_company_not_found(mocker ) -> None:
    ad_client = mocker.Mock()
    ad_client.user_exists.return_value = False

    job = mocker.Mock()
    job.title = "Administrateur systèmes"
    job.organization_unit = "admins"
    job.groups = ["GRP_DEPT_IT"]

    job_repository = mocker.Mock()
    job_repository.get_job.return_value = job

    organization_repository = mocker.Mock()
    organization_repository.get_company.return_value = None

    organization_unit = mocker.Mock()
    organization_unit.ou_name = "Admins"

    organization_repository.get_organization_unit.return_value = organization_unit

    ad_group = mocker.Mock()
    ad_group.distinguished_name = "CN=GRP_DEPT_IT,OU=Groups,DC=lehaneos,DC=lan"

    ad_client.search_group.return_value = ad_group

    identity_builder = mocker.Mock()
    identity_builder.build_username.return_value = "edurand"
    identity_builder.build_display_name.return_value = "Elisa Durand"
    identity_builder.build_email.return_value = "edurand@lehaneos.lan"
    identity_builder.build_upn.return_value = "edurand@lehaneos.lan"

    mocker.patch(
        "lehaneos.core.security.password_generator.PasswordGenerator.generate",
        return_value="Password123!"
    )

    service = UserProvisioningService(
        active_directory_client=ad_client,
        job_repository=job_repository,
        organization_repository=organization_repository,
        account_identity_builder=identity_builder,
    )

    with pytest.raises(ActiveDirectoryCompanyNotFoundError):
        service.provision(
            "Elisa",
            "Durand",
            "system_administrator"
        )

def test_provision_organization_unit_not_found(mocker ) -> None:
    ad_client = mocker.Mock()
    ad_client.user_exists.return_value = False

    job = mocker.Mock()
    job.title = "Administrateur systèmes"
    job.organization_unit = "admins"
    job.groups = ["GRP_DEPT_IT"]

    job_repository = mocker.Mock()
    job_repository.get_job.return_value = job

    company = mocker.Mock()
    company.name = "LehanEOS"
    company.street = "1 rue de la république"
    company.city = "Lyon"
    company.country = "FR"
    company.domain = "lehaneos.lan"
    company.email_domain = "lehaneos.lan"

    organization_repository = mocker.Mock()
    organization_repository.get_company.return_value = company
    organization_repository.get_organization_unit.return_value = None

    ad_group = mocker.Mock()
    ad_group.distinguished_name = "CN=GRP_DEPT_IT,OU=Groups,DC=lehaneos,DC=lan"

    ad_client.search_group.return_value = ad_group

    identity_builder = mocker.Mock()
    identity_builder.build_username.return_value = "edurand"
    identity_builder.build_display_name.return_value = "Elisa Durand"
    identity_builder.build_email.return_value = "edurand@lehaneos.lan"
    identity_builder.build_upn.return_value = "edurand@lehaneos.lan"

    mocker.patch(
        "lehaneos.core.security.password_generator.PasswordGenerator.generate",
        return_value="Password123!"
    )

    service = UserProvisioningService(
        active_directory_client=ad_client,
        job_repository=job_repository,
        organization_repository=organization_repository,
        account_identity_builder=identity_builder,
    )
    with pytest.raises(ActiveDirectoryOrganizationUnitNotFoundError):
        service.provision(
            "Elisa",
            "Durand",
            "system_administrator"
        )

def test_provision_ad_group_not_found(mocker ) -> None:
    ad_client = mocker.Mock()
    ad_client.user_exists.return_value = False

    job = mocker.Mock()
    job.title = "Administrateur systèmes"
    job.organization_unit = "admins"
    job.groups = ["GRP_DEPT_IT"]

    job_repository = mocker.Mock()
    job_repository.get_job.return_value = job

    company = mocker.Mock()
    company.name = "LehanEOS"
    company.street = "1 rue de la république"
    company.city = "Lyon"
    company.country = "FR"
    company.domain = "lehaneos.lan"
    company.email_domain = "lehaneos.lan"

    organization_repository = mocker.Mock()
    organization_repository.get_company.return_value = company

    organization_unit = mocker.Mock()
    organization_unit.ou_name = "Admins"

    organization_repository.get_organization_unit.return_value = organization_unit

    ad_client.search_group.return_value = None

    identity_builder = mocker.Mock()
    identity_builder.build_username.return_value = "edurand"
    identity_builder.build_display_name.return_value = "Elisa Durand"
    identity_builder.build_email.return_value = "edurand@lehaneos.lan"
    identity_builder.build_upn.return_value = "edurand@lehaneos.lan"

    mocker.patch(
        "lehaneos.core.security.password_generator.PasswordGenerator.generate",
        return_value="Password123!"
    )

    service = UserProvisioningService(
        active_directory_client=ad_client,
        job_repository=job_repository,
        organization_repository=organization_repository,
        account_identity_builder=identity_builder,
    )

    with pytest.raises(ActiveDirectoryGroupNotFoundError):
        service.provision(
            "Elisa",
            "Durand",
            "system_administrator"
        )