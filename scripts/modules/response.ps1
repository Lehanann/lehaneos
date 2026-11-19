<#
.SYNOPSIS
Build a standard LehanEOS JSON response

.DESCRIPTION
Creates a standardized response returned to the
Python application through stdout.

.PARAMETER status
Response status (success, warning, error).

.PARAMETER Code
Business response code.

.PARAMETER message
Human-readable message.

.PARAMETER data
Additional response payload.

.OUTPUTS
JSON string.
#>

function New-LehanEOSResponse{
    param(
        [string]$Status,
        [string]$Code,
        [string]$Message,
        [object]$Data
    )

    @{
        status = $Status
        code = $Code
        message = $Message
        data = $Data
     } | ConvertTo-Json -Depth 10

}