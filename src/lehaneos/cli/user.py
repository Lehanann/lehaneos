from pathlib import Path

import typer
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from lehaneos.core.powershell.powershell_runner import PowerShellRunner
from lehaneos.core.ssh.ssh_manager import SSHManager
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.integrations.active_directory.provisioning.builders.account_identity_builder import (
    AccountIdentityBuilder,
)
from lehaneos.integrations.active_directory.provisioning.repositories.job_repository import (
    JobRepository,
)
from lehaneos.integrations.active_directory.provisioning.repositories.organisation_repository import (
    OrganizationRepository,
)
from lehaneos.integrations.active_directory.provisioning.repositories.service_repository import ServiceRepository
from lehaneos.integrations.active_directory.provisioning.services.user_provisioning_service import (
    UserProvisioningService,
)
from lehaneos.settings.settings import settings

app = typer.Typer()

CREATE_USER_SCRIPT = Path(r"C:\lehaneos\Scripts\create-user.ps1")

@app.command("create")
def create_user(
    firstname: str = typer.Option(..., "--firstname" , help="User First name",),
    lastname: str = typer.Option(..., "--lastname" , help="User Last name",),
) -> None:
    """
    Create a new Active Directory user account.

    The command prompts the operator to select a job
    from the configured catalog, generates the user
    provisioning model and executes the PowerShell
    provisioning workflow.

    Args:
        firstname: User first name.
        lastname: User last name.

    Returns:
        None.
    """
    job_identifier = select_job()

    ldap_client = ActiveDirectoryClient()
    ldap_client.connect()

    pwsh_runner = PowerShellRunner(
        SSHManager(
            host=settings.ssh_host,
            port=settings.ssh_port,
            username=settings.ssh_username,
            key_filename=settings.ssh_private_key,
            encoding=settings.ssh_encoding,
        )
    )

    provision_user = UserProvisioningService(
        ldap_client,
        JobRepository(),
        OrganizationRepository(),
        ServiceRepository(),
        AccountIdentityBuilder(),
    )

    try:
        provisioning = provision_user.provision(firstname, lastname, job_identifier)

        response = pwsh_runner.run(CREATE_USER_SCRIPT, provisioning)
        typer.secho(f"✓ {response.message}: {response.data['user']}", fg=typer.colors.GREEN,)
    finally:
        ldap_client.disconnect()


def select_job() -> str:
    """
    Display the available jobs and return the selected job.

    Jobs are loaded from the job repository and displayed
    alphabetically using their title.

    Returns:
        str: Selected job identifier from the job catalog.
    """
    job_repository = JobRepository()

    jobs = job_repository.list_jobs_with_key()

    interactive_choices = [
        Choice(value=job_key, name=job.title)
        for job_key, job in sorted(
            jobs.items(),
            key=lambda item: item[1].title.lower(),
        )
    ]

    return inquirer.select(
        message="Select a job:",
        choices=interactive_choices,
    ).execute()