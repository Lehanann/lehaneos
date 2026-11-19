<#
.SYNOPSIS
Disable an Active Directory user.

.DESCRIPTION
Receives a JSON payload from stdin,
disables the user in Active Directory,
LehanEOS response.
#>

param()
# ===================================================================
# Imports
# ===================================================================
. "C:\lehaneos\modules\Response.ps1"

# ===================================================================
# Input
# ===================================================================
$json = [Console]::In.ReadToEnd()
$request = $json | ConvertFrom-Json

# ===================================================================
# User disable
# ===================================================================
try{
    if ([string]::IsNullOrWhiteSpace($request.target_ou_dn)){
        throw "Organizational unit dn is empty"
    }

    Disable-ADAccount `
        -Identity $request.distinguished_name `        -Confirm:$false `        -ErrorAction Stop

    Move-ADObject -Identity $request.distinguished_name -TargetPath $request.target_ou_dn
    
    $Message = "User successfully disabled and moved on Disabled OU."
# ===================================================================
# Response
# ===================================================================
    New-LehanEOSResponse `
        -status "success" `
        -code "USER_DISABLED" `        -message $Message `        -data @{            
            username = $request.username
            display_name = $request.display_name
        }
}
catch{
    
    New-LehanEOSResponse `
        -status "error" `
        -code "USER_DISABLED_ERROR" `        -message $_.Exception.Message`        -data @{
            username = $request.username
            display_name = $request.display_name
        }
   
}