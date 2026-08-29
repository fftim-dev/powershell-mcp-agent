param(
    [Parameter(Mandatory=$true)]
    [string]$Path,
    [Parameter(Mandatory=$true)]
    [string]$Pattern,
    [int]$First = 50
)

Get-ChildItem -LiteralPath $Path -Filter $Pattern -File | 
    Select-Object -First $First | 
    Select-Object Name, FullName, Length, PSIsContainer | 
    ConvertTo-Json