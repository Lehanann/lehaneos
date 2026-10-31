param(
    [string]$Username,
    [string]$email,
    [string]$FirstName,
    [string]$LastName,
    [string]$DisplayName,
    [string]$OrganizationUnitDN,
    [string]$TemporaryPassword,
    [string]$UserPrincipalName,
    [string[]]$ProxyAddresses,
    [string[]]$GroupsDN,
    [string]$Title,
    [string]$Company,
    [string]$StreetAddress,
    [string]$City,
    [string]$Country    
)

try{
    if ([string]::IsNullOrWhiteSpace($TemporaryPassword))
    {
        throw "Password is empty"
    } 

    $SecurePassword = ConvertTo-SecureString `
        $TemporaryPassword `
        -AsPlainText `
        -Force

    New-ADUser `
        -Name $DisplayName `
        -GivenName $FirstName `
        -Surname $LastName `
        -DisplayName $DisplayName `
        -SamAccountName $Username `
        -UserPrincipalName $UserPrincipalName `
        -EmailAddress $Email `
        -Title $Title `
        -Company $Company `
        -StreetAddress $StreetAddress `
        -City $City `
        -Country $Country `
        -Path $OrganizationUnitDN `
        -AccountPassword $SecurePassword `
        -Enabled $true `
        -ErrorAction Stop

    if ($null -eq $GroupsDN -or $GroupsDN.Count -eq 0)
    {
        throw "Groups DN is empty"
    }else{
        foreach($GroupDN in $GroupsDN)
        {
            Add-ADGroupMember `
                -Identity $GroupDN `
                -Members $Username `
                -ErrorAction Stop
        }        
    }
   
    if ($null -eq $ProxyAddresses -or $ProxyAddresses.Count -eq 0)
    {        
        $Message = "User created without proxy addresses"
    }else{
        Set-ADUser `
            -Identity $Username `
            -Add @{
                proxyAddresses=("SMTP:" + $ProxyAddresses[0])
            } `
            -ErrorAction Stop

        $Message = "User created"
    }
    

    @{
        status = "success"
        code = "USER_CREATED"
        message = $Message
        data = @{ 
            user = $DisplayName
        }
    } | ConvertTo-Json -Depth 5
}
catch {
    @{
        status = "error"
        code = "USER_CREATED_ERROR"
        message = $_.Exception.Message
        data = @{ 
            user = $DisplayName
        }
    } | ConvertTO-Json -depth 5
}
