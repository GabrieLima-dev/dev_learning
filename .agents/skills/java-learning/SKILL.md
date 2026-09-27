---
name: java-learning
description: Conduza a trilha prática persistente de Java deste workspace. Use ao iniciar ou continuar o aprendizado, revisar um exercício concluído, resumir a última sessão ou revisar um tema sob demanda.
---

# Java Learning

Leia primeiro o estado com:

```bash
python3 scripts/learning.py continue
```

Escolha somente o fluxo indicado pela saída. O currículo é a fonte de ordem e pré-requisitos; `scripts/learning.py` é a única forma de alterar o estado.

## Rotas

- Ação `TEACH`: leia [teach-and-assign.md](references/teach-and-assign.md).
- Ação `CREATE_EXERCISE`: retome a criação descrita em [teach-and-assign.md](references/teach-and-assign.md), sem repetir a aula inteira.
- Ação `WAIT_FOR_STUDENT`: diga qual exercício está ativo e aguarde. Se o aluno disser “terminei”, leia [review.md](references/review.md).
- Ação `RESUME_REVIEW`: leia [review.md](references/review.md) e reinicie a verificação; uma execução interrompida não conta como aprovação.
- Pedido de resumo: execute `python3 scripts/learning.py summary` e responda de forma curta.
- Pedido de revisão de tema: leia [revision.md](references/revision.md).
- Ação `TRACK_COMPLETED`: celebre de forma breve e sintetize as competências demonstradas.

## Invariantes

- Não forneça a solução do exercício sem pedido explícito.
- Nunca altere a implementação do aluno durante correção; apenas comentários temporários podem ser inseridos.
- Não avance com base só em testes verdes.
- Não cobre conteúdo posterior à aula atual.
- Mantenha toda escrita dentro deste workspace.
- Use `python3` em Unix/macOS e `py -3` no Windows.
