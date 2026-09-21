[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+$')]
    [string]$Id,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Title,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$AzureUrl,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$ClaudePlanPath
)

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$templatesRoot = Join-Path $projectRoot 'templates'
$itemsRoot = Join-Path $projectRoot 'items'
$stateRoot = Join-Path $projectRoot '.state'

if (-not (Test-Path -LiteralPath $ClaudePlanPath -PathType Leaf)) {
    throw "Plano do Claude não encontrado: $ClaudePlanPath"
}

function ConvertTo-SafeSlug {
    param([string]$Value)
    $normalized = $Value.Normalize([Text.NormalizationForm]::FormD)
    $characters = foreach ($character in $normalized.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($character) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            $character
        }
    }
    $plain = -join $characters
    $slug = [regex]::Replace($plain.ToLowerInvariant(), '[^a-z0-9]+', '-')
    $slug = $slug.Trim('-')
    if ([string]::IsNullOrWhiteSpace($slug)) { $slug = 'item' }
    if ($slug.Length -gt 60) { $slug = $slug.Substring(0, 60).TrimEnd('-') }
    return $slug
}

$slug = ConvertTo-SafeSlug -Value $Title
$itemFolder = Join-Path $itemsRoot "$Id-$slug"
if (Test-Path -LiteralPath $itemFolder) {
    throw "O workspace do item já existe e não será sobrescrito: $itemFolder"
}

$templateNames = @(
    'item.md',
    'reconstruction.md',
    'evidence.md',
    'business-rule.md',
    'code-flow.md',
    'my-understanding.md',
    'review.md',
    'planning.md'
)

foreach ($templateName in $templateNames) {
    $templatePath = Join-Path $templatesRoot $templateName
    if (-not (Test-Path -LiteralPath $templatePath -PathType Leaf)) {
        throw "Template obrigatório ausente: $templatePath"
    }
}

[void](New-Item -ItemType Directory -Path $itemFolder)
foreach ($templateName in $templateNames) {
    Copy-Item -LiteralPath (Join-Path $templatesRoot $templateName) -Destination (Join-Path $itemFolder $templateName)
}

$itemFile = Join-Path $itemFolder 'item.md'
$itemContent = @"
# Item

ID: $Id

Type:

Title: $Title

URL: $AzureUrl

State:

## Description

## Acceptance Criteria

## Context
"@
Set-Content -LiteralPath $itemFile -Value $itemContent -Encoding UTF8

if (-not (Test-Path -LiteralPath $stateRoot -PathType Container)) {
    [void](New-Item -ItemType Directory -Path $stateRoot)
}

$activeItem = [ordered]@{
    workItemId          = $Id
    title               = $Title
    itemFolder          = $itemFolder
    azureUrl            = $AzureUrl
    claudePlanPath      = (Resolve-Path -LiteralPath $ClaudePlanPath).Path
    repositoryPath      = $null
    branch              = $null
    reconstructionStatus = 'NOT_STARTED'
    startedAt           = [DateTimeOffset]::Now.ToString('o')
}

$activeItem | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $stateRoot 'active-item.json') -Encoding UTF8

[PSCustomObject]@{
    WorkItemId = $Id
    ItemFolder = $itemFolder
    StateFile  = Join-Path $stateRoot 'active-item.json'
}

