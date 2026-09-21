[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$results = [Collections.Generic.List[object]]::new()

function Add-Check {
    param([string]$Category, [string]$Check, [bool]$Passed, [string]$Details, [bool]$Warning = $false)
    $status = if ($Passed) { 'PASS' } elseif ($Warning) { 'WARNING' } else { 'FAIL' }
    $script:results.Add([PSCustomObject]@{
        CATEGORY = $Category
        CHECK    = $Check
        STATUS   = $status
        DETAILS  = $Details
    })
}

function Test-SimpleToml {
    param([string]$Path)
    $insideMultiline = $false
    foreach ($line in Get-Content -LiteralPath $Path -Encoding UTF8) {
        $trimmed = $line.Trim()
        if ($insideMultiline) {
            if ($trimmed -eq '"""') { $insideMultiline = $false }
            continue
        }
        if ($trimmed.Length -eq 0 -or $trimmed.StartsWith('#')) { continue }
        if ($trimmed -match '^[A-Za-z0-9_.-]+\s*=\s*"""$') { $insideMultiline = $true; continue }
        if ($trimmed -match '^\[[A-Za-z0-9_.-]+\]$') { continue }
        if ($trimmed -match '^[A-Za-z0-9_.-]+\s*=\s*.+$') { continue }
        return $false
    }
    return -not $insideMultiline
}

$requiredFiles = @(
    'AGENTS.md', 'README.md', '.gitignore',
    '.codex\config.toml', '.codex\hooks.json',
    '.codex\agents\evidence-explorer.toml',
    '.codex\agents\solution-mapper.toml',
    '.codex\agents\learning-assessor.toml',
    '.codex\hooks\session-start.ps1',
    '.codex\hooks\pre-tool-guard.ps1',
    'scripts\list-claude-plans.ps1',
    'scripts\get-ado-item.ps1',
    'scripts\find-mycapital-skills.ps1',
    'scripts\get-git-context.ps1',
    'scripts\new-item-workspace.ps1',
    'scripts\validate-dev-learning.ps1',
    'scripts\run-skill-evals.ps1',
    'scripts\run-hook-tests.ps1',
    'evals\README.md',
    'evals\skill-trigger-cases.jsonl',
    'evals\behavior-cases.jsonl',
    'evals\hook-cases.jsonl',
    'templates\item.md',
    'templates\reconstruction.md',
    'templates\evidence.md',
    'templates\business-rule.md',
    'templates\code-flow.md',
    'templates\my-understanding.md',
    'templates\review.md',
    'templates\planning.md',
    '.state\.gitkeep'
)

foreach ($relativePath in $requiredFiles) {
    $exists = Test-Path -LiteralPath (Join-Path $projectRoot $relativePath) -PathType Leaf
    Add-Check 'STRUCTURE' $relativePath $exists $(if ($exists) { 'presente' } else { 'ausente' })
}

$expectedSkills = @('start-item', 'investigate-item', 'learning-session', 'review-item', 'planning-review', 'consolidate-knowledge')
$skillsRoot = Join-Path $projectRoot '.agents\skills'
$actualSkills = @(Get-ChildItem -LiteralPath $skillsRoot -Directory | Select-Object -ExpandProperty Name | Sort-Object)
$skillSetOk = $actualSkills.Count -eq 6 -and (@($expectedSkills | Where-Object { $actualSkills -notcontains $_ }).Count -eq 0)
Add-Check 'STRUCTURE' 'exactly-six-skills' $skillSetOk ($actualSkills -join ', ')

foreach ($skill in $expectedSkills) {
    $skillPath = Join-Path $skillsRoot "$skill\SKILL.md"
    $valid = $false
    if (Test-Path -LiteralPath $skillPath -PathType Leaf) {
        $lines = @(Get-Content -LiteralPath $skillPath -Encoding UTF8)
        $closing = if ($lines.Count -gt 1) { [Array]::IndexOf($lines, '---', 1) } else { -1 }
        if ($lines[0] -eq '---' -and $closing -gt 1) {
            $frontmatter = $lines[1..($closing - 1)] -join "`n"
            $valid = $frontmatter -match "(?m)^name:\s*$([regex]::Escape($skill))\s*$" -and
                $frontmatter -match '(?m)^description:\s*\S.+'
        }
    }
    Add-Check 'SKILLS' "$skill frontmatter" $valid $(if ($valid) { 'name/description válidos' } else { 'frontmatter inválido' })
}

$requiredReferences = @(
    'investigate-item\references\reconstruction-model.md',
    'investigate-item\references\evidence-model.md',
    'investigate-item\references\claude-plan-analysis.md',
    'investigate-item\references\branch-analysis.md',
    'investigate-item\references\mycapital-architecture.md',
    'investigate-item\references\business-rule.md',
    'investigate-item\references\code-flow.md',
    'investigate-item\references\sql-understanding.md',
    'learning-session\references\learning-levels.md',
    'learning-session\references\question-bank.md',
    'learning-session\references\assessment-rules.md',
    'review-item\references\spaced-review.md',
    'planning-review\references\pcrcv.md',
    'consolidate-knowledge\references\knowledge-model.md'
)
foreach ($reference in $requiredReferences) {
    $exists = Test-Path -LiteralPath (Join-Path $skillsRoot $reference) -PathType Leaf
    Add-Check 'REFERENCES' $reference $exists $(if ($exists) { 'presente' } else { 'ausente' })
}

$obsoleteRootCause = @(Get-ChildItem -LiteralPath $projectRoot -Recurse -File -Filter '*root-cause-gate*' -ErrorAction SilentlyContinue)
$obsoleteMapper = Test-Path -LiteralPath (Join-Path $projectRoot '.codex\agents\system-mapper.toml')
Add-Check 'ARCHITECTURE' 'root-cause-gate removed' ($obsoleteRootCause.Count -eq 0) ($obsoleteRootCause.FullName -join ', ')
Add-Check 'ARCHITECTURE' 'solution-mapper replaces system-mapper' (-not $obsoleteMapper) $(if ($obsoleteMapper) { 'system-mapper ainda existe' } else { 'somente solution-mapper' })

$tomlFiles = @(Get-ChildItem -LiteralPath (Join-Path $projectRoot '.codex') -Recurse -File -Filter '*.toml')
foreach ($toml in $tomlFiles) {
    $valid = Test-SimpleToml -Path $toml.FullName
    $content = Get-Content -Raw -LiteralPath $toml.FullName -Encoding UTF8
    if ($toml.Directory.Name -eq 'agents') {
        $valid = $valid -and $content -match '(?m)^name\s*=' -and $content -match '(?m)^description\s*=' -and
            $content -match '(?m)^developer_instructions\s*=' -and $content -match '(?m)^sandbox_mode\s*=\s*"read-only"'
    }
    Add-Check 'TOML' $toml.Name $valid $(if ($valid) { 'estrutura TOML válida' } else { 'estrutura TOML inválida' })
}

try {
    Get-Content -Raw -LiteralPath (Join-Path $projectRoot '.codex\hooks.json') -Encoding UTF8 | ConvertFrom-Json | Out-Null
    Add-Check 'JSON' 'hooks.json' $true 'JSON válido'
} catch {
    Add-Check 'JSON' 'hooks.json' $false $_.Exception.Message
}

foreach ($jsonlName in @('skill-trigger-cases.jsonl', 'behavior-cases.jsonl', 'hook-cases.jsonl')) {
    $path = Join-Path $projectRoot "evals\$jsonlName"
    $valid = $true
    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $path -Encoding UTF8) {
        $lineNumber++
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $line | ConvertFrom-Json | Out-Null } catch { $valid = $false; break }
    }
    Add-Check 'JSONL' $jsonlName $valid $(if ($valid) { 'todas as linhas válidas' } else { "erro na linha $lineNumber" })
}

$powerShellFiles = @(Get-ChildItem -LiteralPath (Join-Path $projectRoot 'scripts') -File -Filter '*.ps1') +
    @(Get-ChildItem -LiteralPath (Join-Path $projectRoot '.codex\hooks') -File -Filter '*.ps1')
foreach ($scriptFile in $powerShellFiles) {
    $tokens = $null
    $parseErrors = $null
    [void][Management.Automation.Language.Parser]::ParseFile($scriptFile.FullName, [ref]$tokens, [ref]$parseErrors)
    $valid = $parseErrors.Count -eq 0
    Add-Check 'POWERSHELL' $scriptFile.Name $valid $(if ($valid) { 'parse válido' } else { ($parseErrors.Message -join '; ') })
}

$investigate = Get-Content -Raw -LiteralPath (Join-Path $skillsRoot 'investigate-item\SKILL.md') -Encoding UTF8
$planIndex = $investigate.IndexOf('plano Claude selecionado', [StringComparison]::OrdinalIgnoreCase)
$gitIndex = $investigate.IndexOf('usar Git', [StringComparison]::OrdinalIgnoreCase)
Add-Check 'BEHAVIOR' 'plan-before-git' ($planIndex -ge 0 -and $gitIndex -gt $planIndex) "planIndex=$planIndex; gitIndex=$gitIndex"
Add-Check 'BEHAVIOR' 'plan-vs-implementation' ($investigate -match 'Compare plano × implementação') 'comparação explícita'
Add-Check 'BEHAVIOR' 'MyCapital optional' ($investigate -match 'Se houver uma dúvida arquitetural concreta') 'consulta sob demanda'
Add-Check 'BEHAVIOR' 'SQL optional' ($investigate -match 'Somente se restar uma dúvida') 'consulta sob demanda'

$allSkillContent = (Get-ChildItem -LiteralPath $skillsRoot -Recurse -File -Filter '*.md' | ForEach-Object { Get-Content -Raw -LiteralPath $_.FullName -Encoding UTF8 }) -join "`n"
$dangerousPositive = $allSkillContent -match '(?im)^\s*(mvn\s+test|\.\\mvnw\s+test|quarkus:dev|curl\s+https?://|git\s+(?:checkout|switch|pull|push|merge|reset))\b'
Add-Check 'BEHAVIOR' 'no-revalidation-commands' (-not $dangerousPositive) $(if ($dangerousPositive) { 'comando de revalidação/mutação encontrado' } else { 'nenhum comando positivo perigoso' })

$learning = Get-Content -Raw -LiteralPath (Join-Path $skillsRoot 'learning-session\SKILL.md') -Encoding UTF8
$planning = Get-Content -Raw -LiteralPath (Join-Path $skillsRoot 'planning-review\SKILL.md') -Encoding UTF8
$start = Get-Content -Raw -LiteralPath (Join-Path $skillsRoot 'start-item\SKILL.md') -Encoding UTF8
Add-Check 'PEDAGOGY' 'active-recall' ($learning -match 'espere a resposta') 'usuário responde antes da avaliação'
Add-Check 'PEDAGOGY' 'one-question' ($learning -match 'UMA pergunta') 'uma pergunta por vez'
Add-Check 'PEDAGOGY' 'original-answer-preserved' ($start -match 'registre-a literalmente' -and $learning -match 'resposta original') 'preservação explícita'
$levels = Get-Content -Raw -LiteralPath (Join-Path $skillsRoot 'learning-session\references\learning-levels.md') -Encoding UTF8
Add-Check 'PEDAGOGY' 'levels-L1-L5' (($levels -match 'L1') -and ($levels -match 'L2') -and ($levels -match 'L3') -and ($levels -match 'L4') -and ($levels -match 'L5')) 'cinco níveis presentes'
Add-Check 'PEDAGOGY' 'PCRCV' ($planning -match 'Problema, Causa, Regra, Correção e Validação') 'PCRCV presente'

$secretFiles = @(Get-ChildItem -LiteralPath $projectRoot -Recurse -File | Where-Object { $_.Name -match '(?i)^(\.env|.*\.(?:pem|pfx|p12|key))$' })
$secretAssignment = $false
foreach ($file in Get-ChildItem -LiteralPath $projectRoot -Recurse -File) {
    $content = Get-Content -Raw -LiteralPath $file.FullName -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($content -match '(?i)(password|passwd|secret|token|jwt)\s*[:=]\s*["''][A-Za-z0-9+/=_-]{12,}["'']') { $secretAssignment = $true; break }
}
Add-Check 'SECURITY' 'no-obvious-secrets' ($secretFiles.Count -eq 0 -and -not $secretAssignment) $(if ($secretFiles.Count -gt 0 -or $secretAssignment) { 'possível segredo encontrado' } else { 'nenhuma credencial óbvia' })

try {
    $hookOutput = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $projectRoot 'scripts\run-hook-tests.ps1') 2>&1
    $hookPassed = $LASTEXITCODE -eq 0
    Add-Check 'SECURITY' 'hook-tests' $hookPassed $(if ($hookPassed) { 'todos os casos passaram' } else { ($hookOutput -join '; ') })
} catch {
    Add-Check 'SECURITY' 'hook-tests' $false $_.Exception.Message
}

$results | Format-Table -AutoSize -Wrap
$failCount = @($results | Where-Object STATUS -eq 'FAIL').Count
$warningCount = @($results | Where-Object STATUS -eq 'WARNING').Count
"SUMMARY: PASS=$(@($results | Where-Object STATUS -eq 'PASS').Count) FAIL=$failCount WARNING=$warningCount"

if ($failCount -gt 0) { exit 1 }
exit 0
