param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

[PSCustomObject]@{
    path = $Path
    content = Get-Content -LiteralPath $Path -Raw
} | ConvertTo-Json