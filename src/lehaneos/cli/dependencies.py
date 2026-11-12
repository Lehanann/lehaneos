from lehaneos.core.powershell.powershell_runner import PowerShellRunner
from lehaneos.core.ssh.ssh_manager import SSHManager
from lehaneos.integrations.active_directory.ldap_client import ActiveDirectoryClient
from lehaneos.settings.settings import settings

def build_ldap_client() -> ActiveDirectoryClient:
    ldap_client = ActiveDirectoryClient()
    ldap_client.connect()
    return ldap_client

def build_pwsh_runner() -> PowerShellRunner:
    return PowerShellRunner(
        SSHManager(
            host=settings.ssh_host,
            port=settings.ssh_port,
            username=settings.ssh_username,
            key_filename=settings.ssh_private_key,
            encoding=settings.ssh_encoding,
        )
    )