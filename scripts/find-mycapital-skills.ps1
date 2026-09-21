[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Query,

    [ValidateRange(1, 100)]
    [int]$Limit = 20
)

$ErrorActionPreference = 'Stop'
$skillsRoot = 'C:\Users\GabrielLima\.claude\plugins\cache\mycapital\mycapital-backend'

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
    throw "Raiz de Skills MyCapital não encontrada: $skillsRoot"
}

$results = foreach ($file in Get-ChildItem -LiteralPath $skillsRoot -File -Recurse -Filter '*.md') {
    $nameMatch = $file.Name.IndexOf($Query, [StringComparison]::OrdinalIgnoreCase) -ge 0
    $contentMatch = Select-String -LiteralPath $file.FullName -SimpleMatch -Pattern $Query -List -ErrorAction SilentlyContinue
    if ($nameMatch -or $null -ne $contentMatch) {
        $excerpt = if ($null -ne $contentMatch) { $contentMatch.Line.Trim() } else { '[correspondência no nome do arquivo]' }
        if ($excerpt.Length -gt 300) { $excerpt = $excerpt.Substring(0, 300) + '…' }
        [PSCustomObject]@{
            Name     = $file.Name
            FullPath = $file.FullName
            Match    = $excerpt
        }
    }
}

$results | Select-Object -First $Limit

