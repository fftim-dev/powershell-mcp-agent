param(
    [Parameter(Mandatory=$true)]
    [string]$PathsJson
)

$Paths = $PathsJson | ConvertFrom-Json

$results = foreach ($Path in $Paths) {
    [PSCustomObject]@{
        path = $Path
        content = Get-Content -LiteralPath $Path -Raw
    }
}

$results | ConvertTo-Json