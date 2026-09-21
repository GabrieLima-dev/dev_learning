[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$evalRoot = Join-Path $projectRoot 'evals'
$failed = $false

function Read-JsonLines {
    param([Parameter(Mandatory = $true)][string]$Path)
    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $lineNumber++
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try {
            $line | ConvertFrom-Json
        } catch {
            throw "JSONL inválido em $Path, linha $lineNumber`: $($_.Exception.Message)"
        }
    }
}

function Write-EvalResult {
    param($Id, $Expected, $Observed, $Result, $Notes)
    [PSCustomObject]@{
        EVAL     = $Id
        EXPECTED = $Expected
        OBSERVED = $Observed
        RESULT   = $Result
        NOTES    = $Notes
    }
}

$triggerPath = Join-Path $evalRoot 'skill-trigger-cases.jsonl'
$behaviorPath = Join-Path $evalRoot 'behavior-cases.jsonl'
$hookPath = Join-Path $evalRoot 'hook-cases.jsonl'

try {
    $triggerCases = @(Read-JsonLines -Path $triggerPath)
    $behaviorCases = @(Read-JsonLines -Path $behaviorPath)
    $hookCases = @(Read-JsonLines -Path $hookPath)
    Write-EvalResult 'jsonl-parse' '3 arquivos JSONL válidos' '3 arquivos válidos' 'PASS' 'Validação sintática concluída.'
} catch {
    Write-EvalResult 'jsonl-parse' '3 arquivos JSONL válidos' $_.Exception.Message 'FAIL' 'Corrija as definições.'
    exit 1
}

foreach ($case in $triggerCases) {
    if ($null -eq $case.expected_skill) {
        Write-EvalResult $case.id 'nenhuma Skill obrigatória' 'caso negativo registrado' 'PASS' 'A seleção viva depende do Codex.'
        continue
    }
    $skillFile = Join-Path $projectRoot ".agents\skills\$($case.expected_skill)\SKILL.md"
    if (Test-Path -LiteralPath $skillFile -PathType Leaf) {
        Write-EvalResult $case.id $case.expected_skill 'Skill existe e está endereçável' 'PASS' 'Não mede a seleção do modelo.'
    } else {
        $failed = $true
        Write-EvalResult $case.id $case.expected_skill 'Skill ausente' 'FAIL' $skillFile
    }
}

foreach ($case in $behaviorCases) {
    $skillFile = Join-Path $projectRoot ".agents\skills\$($case.skill)\SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        $failed = $true
        Write-EvalResult $case.id 'contrato presente' 'Skill ausente' 'FAIL' $skillFile
        continue
    }
    $content = Get-Content -Raw -LiteralPath $skillFile -Encoding UTF8
    $missing = @($case.must_contain | Where-Object { $content.IndexOf("$_", [StringComparison]::OrdinalIgnoreCase) -lt 0 })
    $forbidden = @($case.must_not_contain | Where-Object { $content.IndexOf("$_", [StringComparison]::OrdinalIgnoreCase) -ge 0 })
    if ($missing.Count -eq 0 -and $forbidden.Count -eq 0) {
        Write-EvalResult $case.id 'contrato estático atendido' 'termos obrigatórios presentes; proibidos ausentes' 'PASS' 'Avaliação determinística do arquivo.'
    } else {
        $failed = $true
        Write-EvalResult $case.id 'contrato estático atendido' "ausentes=$($missing -join ', '); proibidos=$($forbidden -join ', ')" 'FAIL' 'O comportamento descrito diverge do caso.'
    }
}

Write-EvalResult 'live-codex-behavior' 'seleção e execução observadas em sessão isolada' 'não executado' 'WARNING' 'O runner valida contratos e JSONL; não invoca modelo nem Azure automaticamente.'

if ($failed) { exit 1 }
exit 0

