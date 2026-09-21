[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$guardPath = Join-Path $projectRoot '.codex\hooks\pre-tool-guard.ps1'
$casesPath = Join-Path $projectRoot 'evals\hook-cases.jsonl'
$failed = $false

if (-not (Test-Path -LiteralPath $guardPath -PathType Leaf)) {
    throw "Hook não encontrado: $guardPath"
}

$cases = @()
$lineNumber = 0
foreach ($line in Get-Content -LiteralPath $casesPath -Encoding UTF8) {
    $lineNumber++
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    try {
        $cases += $line | ConvertFrom-Json
    } catch {
        throw "JSONL inválido em $casesPath, linha $lineNumber`: $($_.Exception.Message)"
    }
}

foreach ($case in $cases) {
    $payload = [ordered]@{
        session_id      = 'hook-test'
        turn_id         = 'hook-test-turn'
        cwd             = $case.cwd
        hook_event_name = 'PreToolUse'
        tool_name       = $case.tool_name
        tool_use_id     = $case.id
        tool_input      = [ordered]@{ command = $case.command }
    } | ConvertTo-Json -Depth 8 -Compress

    $rawOutput = @($payload | & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $guardPath 2>&1)
    $exitCode = $LASTEXITCODE
    $observed = 'ALLOW'
    $notes = ''

    if ($rawOutput.Count -gt 0) {
        try {
            $response = ($rawOutput -join [Environment]::NewLine) | ConvertFrom-Json
            if ($response.hookSpecificOutput.permissionDecision -eq 'deny') {
                $observed = 'DENY'
                $notes = $response.hookSpecificOutput.permissionDecisionReason
            } else {
                $observed = 'INVALID_OUTPUT'
                $notes = $rawOutput -join ' '
            }
        } catch {
            $observed = 'ERROR'
            $notes = $rawOutput -join ' '
        }
    }
    if ($exitCode -ne 0) {
        $observed = 'ERROR'
        $notes = "exit=$exitCode; $notes"
    }

    $result = if ($observed -eq $case.expected) { 'PASS' } else { 'FAIL' }
    if ($result -eq 'FAIL') { $failed = $true }
    [PSCustomObject]@{
        TEST     = $case.id
        EXPECTED = $case.expected
        OBSERVED = $observed
        RESULT   = $result
        NOTES    = $notes
    }
}

$probePath = Join-Path $projectRoot '.state\hook-write-probe.tmp'
try {
    Set-Content -LiteralPath $probePath -Value 'DEV_LEARNING write probe' -Encoding UTF8
    $probeOk = Test-Path -LiteralPath $probePath -PathType Leaf
} catch {
    $probeOk = $false
    $probeError = $_.Exception.Message
} finally {
    if (Test-Path -LiteralPath $probePath) {
        Remove-Item -LiteralPath $probePath -Force
    }
}

$probeResult = if ($probeOk) { 'PASS' } else { 'FAIL' }
if (-not $probeOk) { $failed = $true }
[PSCustomObject]@{
    TEST     = 'filesystem-write-inside-project'
    EXPECTED = 'ALLOW'
    OBSERVED = if ($probeOk) { 'ALLOW' } else { 'ERROR' }
    RESULT   = $probeResult
    NOTES    = if ($probeOk) { 'Arquivo temporário criado e removido dentro do DEV_LEARNING.' } else { $probeError }
}

if ($failed) { exit 1 }
exit 0

