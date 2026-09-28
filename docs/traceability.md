# Rastreabilidade da V1

| Requisitos | Implementação |
|---|---|
| RF-001–003, RNF-002/003/005/008 | `.learning/progress.json`; comandos `init`, `continue`, `status`; testes de retomada. |
| RF-004–006, RN-004/011 | currículo com objetivo/pré-requisitos; fluxo `teach`; skill pedagógica. |
| RF-007–010, RN-001/009/010 | skill cria starter + JUnit + TODO; `assign` valida caminhos e para em espera. |
| Diagnóstico inicial opcional | skill informa a opção; `skip-diagnostic` registra o salto, preserva os arquivos e leva à primeira aula regular sem dispensar nenhuma aula posterior. |
| RF-011–016, RN-002/003/006/007/012 | Maven/JUnit, `review-start`, `review-result`, marcadores temporários e preservação do código. |
| RF-017 | `.learning/session.md` e comando `summary`. |
| RF-018, RN-008 | `revision-start`/`revision-end` preservam posição principal. |
| RF-019/020, RN-005 | checkpoints obrigatórios e currículo cumulativo. |
| RNF-001 | regras de clareza no `AGENTS.md` e skill. |
| RNF-004 | resolução segura de caminhos e escopo no `AGENTS.md`. |
| RNF-006/007/009 | separação currículo/estado/avaliação; Maven + Java 25 + JUnit. |

## Critérios de produto cobertos

- Workspace já possui estado inicial consultável.
- Continuidade é derivada apenas do estado.
- Preparação separa explicação, starter e testes.
- Revisão combina execução objetiva e análise.
- Correção mantém o exercício ativo.
- Aprovação remove feedback, conclui e aponta a próxima aula.
- Resumo e revisão não alteram indevidamente a trilha.
