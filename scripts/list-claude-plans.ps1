[CmdletBinding()]
param(
    [ValidateRange(1, 100)]
    [int]$Limit = 10
)

$ErrorActionPreference = 'Stop'
$plansRoot = 'C:\Users\GabrielLima\.claude\plans'

if (-not (Test-Path -LiteralPath $plansRoot -PathType Container)) {
    throw "Diretório de planos não encontrado: $plansRoot"
}

$index = 0
Get-ChildItem -LiteralPath $plansRoot -File -Recurse |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First $Limit |
    ForEach-Object {
        $index++
        [PSCustomObject]@{
            Index         = $index
            Name          = $_.Name
            LastWriteTime = $_.LastWriteTime
            FullPath      = $_.FullName
        }
    }

