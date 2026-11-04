from lehaneos.core.security.password_generator import PasswordGenerator
from lehaneos.integrations.active_directory.exceptions import (
    ActiveDirectoryUserAlreadyExistsError,
    ActiveDirectoryJobNotFoundError,
    ActiveDirectoryOrganizationUnitNotFoundError,
    ActiveDirectoryCompanyNotFoundError,
    ActiveDirectoryGroupNotFoundError,
)
from lehaneos.integrations.active_directory.provisioning.builders.account_identity_builder import AccountIdentityBuilder
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.repositories.job_repository import JobRepository
from lehaneos.integrations.active_directory.provisioning.repositories.organisation_repository import OrganizationRepository
from lehaneos.integrations.active_directory.provisioning.schemas.user_account_provisioning import UserAccountProvisioning
from lehaneos.settings.settings import settings


class UserProvisioningService:

    def __init__(self,
                 active_directory_client: ActiveDirectoryClient,
                 job_repository: JobRepository,
                 organization_repository: OrganizationRepository,
                 account_identity_builder: AccountIdentityBuilder
                 ) -> None:
        self.active_directory_client = active_directory_client
        self.job_repository = job_repository
        self.organization_repository = organization_repository
        self.account_identity_builder = account_identity_builder

    def provision(self,first_name:str, last_name:str, job_name: str) -> UserAccountProvisioning:
        try:
            # ======================================================
            # User Identity
            # ======================================================
            # Build username
            username = self.account_identity_builder.build_username(first_name,last_name)
            # Check username already exists if exists causes an error
            if self.active_directory_client.user_exists(username):
                raise ActiveDirectoryUserAlreadyExistsError("User already exists.")

            # ======================================================
            # Job Information
            # ======================================================
            # Get job and check exists if not found causes an error
            job = self.job_repository.get_job(job_name)
            if job is None:
                raise ActiveDirectoryJobNotFoundError("Job not found.")

            # ======================================================
            # Company Information
            # ======================================================
            # Get company and check if is not None
            company = self.organization_repository.get_company()
            if company is None:
                raise ActiveDirectoryCompanyNotFoundError("Company not found.")

            # ======================================================
            # User Account Construction
            # ======================================================
            # Build display name
            display_name = self.account_identity_builder.build_display_name(first_name, last_name)

            # Build UPN
            user_principal_name = self.account_identity_builder.build_upn(company.domain, first_name, last_name)

            # Build user email
            email = self.account_identity_builder.build_email(company.email_domain, first_name, last_name)

            # ======================================================
            # Active Directory resolution
            # ======================================================
            # Get organization unit assigned to user (groups: users, admins or service accounts)
            organization_unit = self.organization_repository.get_organization_unit(job.organization_unit)
            if organization_unit is None:
                raise ActiveDirectoryOrganizationUnitNotFoundError("Organization unit not found.")

            # Build groups_dn
            groups_dn: list[str] = []
            for group in job.groups:
                ad_group = self.active_directory_client.search_group(group)
                if ad_group is None:
                    raise ActiveDirectoryGroupNotFoundError("Group not found.")
                groups_dn.append(ad_group.distinguished_name)

            # ======================================================
            # Build provisioning model
            # ======================================================
            user_account_provisioning = UserAccountProvisioning(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                display_name=display_name,
                organization_unit_dn=f"OU={organization_unit.ou_name},{settings.full_root_ou}",
                temporary_password=PasswordGenerator.generate(),
                user_principal_name=user_principal_name,
                proxy_addresses=[email],
                groups_dn=groups_dn,
                title=job.title,
                company=company.name,
                street_address=company.street,
                city=company.city,
                country=company.country,
            )
            return user_account_provisioning

        finally:
            self.active_directory_client.disconnect()
