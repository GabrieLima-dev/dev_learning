[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$RepositoryPath,

    [string]$Branch,

    [string]$BaseBranch,

    [ValidateRange(100, 20000)]
    [int]$MaxDiffLines = 2000
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $RepositoryPath -PathType Container)) {
    throw "Repositório não encontrado: $RepositoryPath"
}

function Invoke-GitRead {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    $output = & git -C $RepositoryPath @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Falha em git $($Arguments -join ' '): $($output -join [Environment]::NewLine)"
    }
    return @($output | ForEach-Object { "$_" })
}

$inside = (Invoke-GitRead -Arguments @('rev-parse', '--is-inside-work-tree')) -join ''
if ($inside.Trim() -ne 'true') {
    throw "O caminho não é um working tree Git: $RepositoryPath"
}

$currentBranch = ((Invoke-GitRead -Arguments @('branch', '--show-current')) -join '').Trim()
$targetBranch = if ([string]::IsNullOrWhiteSpace($Branch)) { $currentBranch } else { $Branch }

if (-not [string]::IsNullOrWhiteSpace($Branch)) {
    [void](Invoke-GitRead -Arguments @('rev-parse', '--verify', $Branch))
}
if (-not [string]::IsNullOrWhiteSpace($BaseBranch)) {
    [void](Invoke-GitRead -Arguments @('rev-parse', '--verify', $BaseBranch))
}

$status = Invoke-GitRead -Arguments @('status', '--short')
$commits = Invoke-GitRead -Arguments @('log', '-20', '--date=iso-strict', '--pretty=format:%H%x09%ad%x09%s')

if (-not [string]::IsNullOrWhiteSpace($BaseBranch)) {
    $range = "$BaseBranch...$targetBranch"
    $changedFiles = Invoke-GitRead -Arguments @('diff', '--name-status', $range)
    $diff = Invoke-GitRead -Arguments @('diff', '--no-ext-diff', '--unified=3', $range)
} else {
    $changedFiles = @(
        Invoke-GitRead -Arguments @('diff', '--name-status')
        Invoke-GitRead -Arguments @('diff', '--cached', '--name-status')
    ) | Select-Object -Unique
    $diff = @(
        Invoke-GitRead -Arguments @('diff', '--no-ext-diff', '--unified=3')
        Invoke-GitRead -Arguments @('diff', '--cached', '--no-ext-diff', '--unified=3')
    )
}

$diffWasTruncated = $diff.Count -gt $MaxDiffLines
if ($diffWasTruncated) {
    $diff = @($diff | Select-Object -First $MaxDiffLines)
}

[PSCustomObject]@{
    repositoryPath   = (Resolve-Path -LiteralPath $RepositoryPath).Path
    currentBranch    = $currentBranch
    analyzedBranch   = $targetBranch
    baseBranch       = $BaseBranch
    status           = $status
    commits          = $commits
    changedFiles     = $changedFiles
    diff             = $diff
    diffWasTruncated = $diffWasTruncated
} | ConvertTo-Json -Depth 8

