<#
.SYNOPSIS
Create an Active Directory user.

.DESCRIPTION
Receives a JSON payload from stdin,
creates the user in Active Directory,
assigns groups and retruns a standardized
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
# Variables
# ===================================================================


# ===================================================================
# Main
# ===================================================================
try{
    if ([string]::IsNullOrWhiteSpace($request.temporary_password)){
        throw "Password is empty"
    }
    $SecurePassword = ConvertTo-SecureString `
        $request.temporary_password `
        -AsPlainText `
        -Force

    $params = @{
        SamAccountName = $request.username
        Name = $request.display_name
        EmailAddress = $request.email
        GivenName = $request.first_name
        Surname = $request.last_name
        DisplayName = $request.display_name
        Path = $request.organization_unit_dn        
        UserPrincipalName = $request.user_principal_name
        AccountPassword = $SecurePassword
        Title = $request.title
        Department = $request.department_name
        Office = $request.service_name
        Company = $request.company
        StreetAddress = $request.street_address
        City = $request.city
        Country = $request.country
        Enabled = $true 
    }

    if($request.service_name){
        $params.Office = $request.service_name
    }

# ===================================================================
# User creation
# ===================================================================
    New-ADUser @params `
        -ErrorAction Stop

    if ($null -eq $request.groups_dn -or $request.groups_dn.Count -eq 0)
    {
        throw "Groups DN is empty"
    }else{
        foreach($GroupDN in $request.groups_dn)
        {
            Add-ADGroupMember `
                -Identity $GroupDN `
                -Members $request.username `
                -ErrorAction Stop
        }        
    }
   
    if ($null -eq $request.proxy_addresses -or $request.proxy_addresses.Count -eq 0)
    {        
        $Message = "User created without proxy addresses"
    }else{
        Set-ADUser `
            -Identity $request.username `
            -Add @{
                proxyAddresses=("SMTP:" + $request.proxy_addresses[0])
            } `
            -ErrorAction Stop

        $Message = "User created"
    }

# ===================================================================
# Response
# ===================================================================
    New-LehanEOSResponse `
        -status "success" `
        -Code "USER CREATED" `        -message $Message `        -data @{
            user = $request.display_name
        }
}
catch{
    
    New-LehanEOSResponse `
        -status "error" `
        -Code "USER_CREATED_ERROR" `        -message $_.Exception.Message`        -data @{
            user = $request.display_name
        }
   
}
