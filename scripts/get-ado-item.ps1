[CmdletBinding(DefaultParameterSetName = 'ById')]
param(
    [Parameter(Mandatory = $true, ParameterSetName = 'ByUrl')]
    [ValidateNotNullOrEmpty()]
    [string]$Url,

    [Parameter(Mandatory = $true, ParameterSetName = 'ById')]
    [ValidateRange(1, [int]::MaxValue)]
    [int]$Id
)

$ErrorActionPreference = 'Stop'

if ($PSCmdlet.ParameterSetName -eq 'ByUrl') {
    $match = [regex]::Match($Url, '(?i)(?:workitems|_workitems/edit)/(\d+)')
    if (-not $match.Success) {
        $match = [regex]::Match($Url, '(\d+)(?:/)?(?:\?.*)?$')
    }
    if (-not $match.Success) {
        throw 'Não foi possível extrair o ID do Work Item da URL.'
    }
    $workItemId = [int]$match.Groups[1].Value
} else {
    $workItemId = $Id
}

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    throw 'Azure CLI não encontrada. Instale/configure-a manualmente; este script não instala ferramentas.'
}

$raw = & az boards work-item show --id $workItemId --output json 2>&1
if ($LASTEXITCODE -ne 0) {
    $message = $raw -join [Environment]::NewLine
    throw "Falha na consulta read-only do Work Item. Verifique login, organização e extensão azure-devops. $message"
}

$item = ($raw -join [Environment]::NewLine) | ConvertFrom-Json
$fields = $item.fields
$assigned = $fields.'System.AssignedTo'
if ($assigned -is [string]) {
    $assignedTo = $assigned
} elseif ($null -ne $assigned) {
    $assignedTo = $assigned.displayName
} else {
    $assignedTo = $null
}

$relations = @()
foreach ($relation in @($item.relations)) {
    $relations += [PSCustomObject]@{
        rel   = $relation.rel
        url   = $relation.url
        name  = $relation.attributes.name
    }
}

$resolvedUrl = $null
if ($null -ne $item._links -and $null -ne $item._links.html) {
    $resolvedUrl = $item._links.html.href
}
if ([string]::IsNullOrWhiteSpace($resolvedUrl) -and $PSCmdlet.ParameterSetName -eq 'ByUrl') {
    $resolvedUrl = $Url
}

[PSCustomObject]@{
    id                 = $item.id
    title              = $fields.'System.Title'
    workItemType       = $fields.'System.WorkItemType'
    state              = $fields.'System.State'
    description        = $fields.'System.Description'
    acceptanceCriteria = $fields.'Microsoft.VSTS.Common.AcceptanceCriteria'
    tags               = $fields.'System.Tags'
    assignedTo         = $assignedTo
    relations          = $relations
    url                = $resolvedUrl
} | ConvertTo-Json -Depth 8

