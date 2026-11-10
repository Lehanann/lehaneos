from pathlib import Path

from lehaneos.core.logging_config import configure_logging
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

# import paramiko

configure_logging()

# print(dir(paramiko))
"""
ssh_client = SSHManager(
    host=settings.ssh_host,
    port=settings.ssh_port,
    username=settings.ssh_username,
    key_filename=settings.ssh_private_key,
    encoding=settings.ssh_encoding,
)

ssh_client.connect()
result = ssh_client.execute_command("Write-output 'Hé t'es quité'")
ssh_client.disconnect()

print(result.stdout)
print(result.stderr)
print(result.exit_status)

ssh_client.disconnect()


test = {
            "Username": "jmoulin",
            "DisplayName": "Jean Moulin",
            "ProxyAddresses": ["jmoulin@test.fr","test@test.fr"],
            "GroupsDN": ["admin","testeur"],
        }
"""

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

path_script = Path(r"C:\lehaneos\Scripts\create-user.ps1")

provisioning = provision_user.provision("Jean Philippe", "Delmotte", "general_director")
#provisioning = provision_user.provision("Mickaël", "Vial", "information_systems_manager")


response = pwsh_runner.run(path_script, provisioning)
print("RETURN", response)
ldap_client.disconnect()
