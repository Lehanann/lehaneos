<#
.SYNOPSIS
Enable an Active Directory user.

.DESCRIPTION
Receives a JSON payload from stdin,
enables the disabled user in Active Directory,
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
# Password reset
# ===================================================================
try{
    if ([string]::IsNullOrWhiteSpace($request.new_password)){
        throw "Password is empty"
    }
    $SecurePassword = ConvertTo-SecureString `
        $request.new_password `
        -AsPlainText `
        -Force

   Set-ADAccountPassword `
        -Identity $request.username `        -Reset `        -NewPassword $SecurePassword `        -Confirm:$false `        -ErrorAction Stop
     $Message = "Password successfully reset"

# ===================================================================
# Response
# ===================================================================
    New-LehanEOSResponse `
        -status "success" `
        -code "PASSWORD_RESET" `        -message $Message `        -data @{
            username = $request.username
        }
}
catch{
    
    New-LehanEOSResponse `
        -status "error" `
        -code "PASSWORD_RESET_ERROR" `        -message $_.Exception.Message`        -data @{
            username = $request.username
        }
   
}