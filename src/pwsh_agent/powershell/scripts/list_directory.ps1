param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

Get-ChildItem -LiteralPath $Path |
    Select-Object Name, FullName, Length, PSIsContainer |
    ConvertTo-Json