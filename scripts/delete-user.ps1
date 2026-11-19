<#
.SYNOPSIS
Delete an Active Directory user.

.DESCRIPTION
Receives a JSON payload from stdin,
deletes the user in Active Directory,
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
# User deletion
# ===================================================================
try{

    Remove-ADUser `
        -Identity $request.distinguished_name `        -Confirm:$false `        -ErrorAction Stop
    
    $Message = "User successfully deleted"
# ===================================================================
# Response
# ===================================================================
    New-LehanEOSResponse `
        -status "success" `
        -code "USER_DELETED" `        -message $Message `        -data @{
            display_name=$request.display_name
            username = $request.username
        }
}
catch{
    
    New-LehanEOSResponse `
        -status "error" `
        -code "USER_DELETED_ERROR" `        -message $_.Exception.Message`        -data @{
            display_name = $request.display_name
            username = $request.username
        }
   
}