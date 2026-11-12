from pathlib import Path

import typer
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from lehaneos.cli.dependencies import build_ldap_client, build_pwsh_runner
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
from lehaneos.integrations.active_directory.provisioning.services.user_deletion_service import UserDeletionService
from lehaneos.integrations.active_directory.provisioning.services.user_disable_service import UserDisableService
from lehaneos.integrations.active_directory.provisioning.services.user_enable_service import UserEnableService
from lehaneos.integrations.active_directory.provisioning.services.user_reset_password_service import UserResetPasswordService
from lehaneos.integrations.active_directory.provisioning.services.user_provisioning_service import (
    UserProvisioningService,
)
from lehaneos.settings.settings import settings

app = typer.Typer()

CREATE_USER_SCRIPT = Path(r"C:\lehaneos\Scripts\create-user.ps1")
DELETE_USER_SCRIPT = Path(r"C:\lehaneos\Scripts\delete-user.ps1")
DISABLE_USER_SCRIPT = Path(r"C:\lehaneos\Scripts\disable-user.ps1")
ENABLE_USER_SCRIPT = Path(r"C:\lehaneos\Scripts\enable-user.ps1")
RESET_PASSWORD_SCRIPT = Path(r"C:\lehaneos\Scripts\reset-password.ps1")

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

    ldap_client = build_ldap_client()
    pwsh_runner = build_pwsh_runner()

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

@app.command("delete")
def delete_user(username: str = typer.Option(
    ...,"--username" , help="User username")
) -> None:
    """
    Delete an Active Directory user account.

    The command prompts the operator to enter the username to delete the account in Active Directory.

    Args:
        username: User username.

    Returns:
        None.
    """
    ldap_client = build_ldap_client()
    pwsh_runner = build_pwsh_runner()

    deletion_service = UserDeletionService(ldap_client)

    try:
        deleted_user = deletion_service.delete(username)
        response = pwsh_runner.run(DELETE_USER_SCRIPT, deleted_user)
        typer.secho(f"✓ {response.message}: {response.data['username']}", fg=typer.colors.GREEN, )
    finally:
        ldap_client.disconnect()

@app.command("disable")
def disable_user(username: str = typer.Option(
    ...,"--username" , help="User username"
)) -> None:
    """
    Disable an Active Directory user account.

    The command prompts the operator to enter the username to disable the account in Active Directory.

    Args:
        username: User username.

    Returns:
        None.
    """
    ldap_client = build_ldap_client()
    pwsh_runner = build_pwsh_runner()

    disable_service = UserDisableService(ldap_client)

    try:
        disabled_user = disable_service.disable(username)
        response = pwsh_runner.run(DISABLE_USER_SCRIPT, disabled_user)
        typer.secho(f"✓ {response.message}: {response.data['username']}", fg=typer.colors.GREEN, )
    finally:
        ldap_client.disconnect()

@app.command("enable")
def enable_user(username: str = typer.Option(
    ...,"--username" , help="User username"
)) -> None:
    """
    Enable an Active Directory user account.

    The command prompts the operator to enter the username to enable the account in Active Directory.

    Args:
        username: User username.

    Returns:
        None.
    """
    ldap_client = build_ldap_client()
    pwsh_runner = build_pwsh_runner()

    enable_service = UserEnableService(ldap_client)

    try:
        enabled_user = enable_service.enable(username)
        response = pwsh_runner.run(ENABLE_USER_SCRIPT, enabled_user)
        typer.secho(f"✓ {response.message}: {response.data['username']}", fg=typer.colors.GREEN, )
    finally:
        ldap_client.disconnect()

@app.command("reset-password")
def reset_password(username: str = typer.Option(
    ...,"--username" , help="User username"
)) -> None:
    """
    Reset password an Active Directory user account.

    The command prompts the operator to enter the username to reset password of the account in Active Directory.

    Args:
        username: User username.

    Returns:
        None.
    """
    ldap_client = build_ldap_client()
    pwsh_runner = build_pwsh_runner()

    user_reset_password_service = UserResetPasswordService(ldap_client)

    try:
        reset_password_user = user_reset_password_service.reset_password(username)
        typer.secho(f"✓ New Temporary Password: {reset_password_user.new_password}", fg=typer.colors.BRIGHT_YELLOW, )

        response = pwsh_runner.run(RESET_PASSWORD_SCRIPT, reset_password_user)
        typer.secho(f"✓ {response.message}: {response.data['username']}", fg=typer.colors.GREEN, )
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