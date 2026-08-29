param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

Get-ChildItem -LiteralPath $Path -File | 
    Select-Object Name, FullName, Length, PSIsContainer | 
    ConvertTo-Json