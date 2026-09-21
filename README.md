# DEV_LEARNING - TESTE SALA

## Objetivo

Ambiente pessoal para reconstruir soluções de PIBs e BUGs já concluídos e transformar o trabalho real em aprendizagem ativa. O foco é entender o problema, a decisão, a regra, o fluxo do código, a alteração e por que ela funciona.

## Claude x Codex

Claude auxilia no desenvolvimento, implementação e validação original. Depois, Codex lê o item, o plano e a branch para reconstruir a solução, testar o entendimento do usuário, apoiar revisões e preparar explicações de Planning. O Codex não revalida nem reimplementa a correção.

## Fluxo principal

```text
$start-item
    ↓
$investigate-item
    ↓
$learning-session
    ↓
$review-item
    ↓
$planning-review
    ↓
$consolidate-knowledge
```

## Fontes

Azure DevOps → plano do Claude → Git/branch → código → Skills MyCapital sob demanda → SQL opcional.

## Segurança

Somente `C:\Users\GabrielLima\dev-learning` pode ser alterado. Repositórios corporativos, `.claude`, Azure DevOps e Azure SQL são somente leitura. Não são executados testes, endpoints ou reprodução do BUG para validar novamente uma solução já concluída.

## Estrutura

- `.agents/skills`: as seis Skills do fluxo.
- `.codex/agents`: subagentes read-only.
- `.codex/hooks`: contexto inicial e proteção contra mutações.
- `scripts`: coleta segura, criação de workspace e validação.
- `templates`: registros de cada item.
- `items`, `reviews`, `knowledge`: aprendizado preservado.

## Como validar

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-dev-learning.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\run-hook-tests.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\run-skill-evals.ps1
```

## Como iniciar

Abra esta pasta no VS Code, inicie o Codex nela e use:

```text
$start-item
```

## Futuro

Uma `learning-retro` poderá ser considerada após existir histórico real de 5–10 itens; ela não faz parte da V3.

