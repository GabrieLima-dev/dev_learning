# Evals do DEV_LEARNING

- `skill-trigger-cases.jsonl`: exemplos positivos e negativos de seleção de Skill.
- `behavior-cases.jsonl`: contratos observáveis de cada workflow.
- `hook-cases.jsonl`: comandos simulados permitidos e bloqueados.

Execute `scripts/run-skill-evals.ps1` para validar JSONL, Skills esperadas e contratos estáticos. Esse runner não afirma ter medido comportamento de modelo: uma avaliação viva do Codex é registrada como limitação quando não é executada.

Execute `scripts/run-hook-tests.ps1` para alimentar o hook com JSON simulado. Nenhum comando de caso é realmente executado.

