# DEV_LEARNING — Constituição do projeto

## Propósito

Este projeto transforma PIBs e BUGs já resolvidos em aprendizado técnico e de negócio. Claude participa da investigação, implementação e validação originais; Codex reconstrói e ensina a solução depois que o trabalho terminou. Não reabra o debugging nem trate este repositório como ambiente de implementação corporativa.

## Fluxo obrigatório

1. Leia o item do Azure DevOps para entender problema e contexto.
2. Leia somente o plano do Claude selecionado antes de examinar o Git.
3. Analise branch, diff, commits e código relevante em modo somente leitura.
4. Compare intenção do plano com implementação real.
5. Consulte Skills MyCapital apenas quando o código exigir contexto arquitetural.
6. Consulte SQL apenas se as fontes anteriores não explicarem um dado ou regra.
7. Reconstrua problema, estratégia, fluxo, regra e por que a alteração resolve.
8. Pare quando houver entendimento suficiente; não sobreinvestigue.

Use divulgação progressiva: carregue apenas a Skill, referência, arquivo e trecho necessários ao passo atual.

## Aprendizagem

- Use recuperação ativa antes de explicar: faça UMA pergunta por vez e espere a resposta.
- Preserve literalmente toda resposta original do usuário; nunca a reescreva como se fosse dele nem sobrescreva `my-understanding.md`.
- Ensine somente conceitos ligados ao item real.
- Classifique afirmações relevantes como `VERIFIED`, `INFERRED`, `UNKNOWN` ou `GENERAL_KNOWLEDGE` e cite arquivos, classes, métodos, commits, queries ou Skills quando possível.
- Não encontrado não significa não existe.
- Plano Claude não significa implementação final.
- Comportamento implementado não significa automaticamente regra oficial de negócio.
- Não invente regras de negócio.

## Segurança

Escreva somente em `C:\Users\GabrielLima\dev-learning`. Tudo fora dessa raiz é somente leitura, incluindo `.claude`, planos, Skills MyCapital, `C:\java_projects`, Azure DevOps e Azure SQL.

Git é somente leitura. São aceitáveis `status`, `log`, `show`, `diff`, `branch --show-current`, `rev-parse`, `blame`, `grep`, `ls-files` e `remote -v`. Não execute comandos Git mutáveis.

Azure DevOps é somente leitura. Não crie, atualize, exclua, aprove, vote, faça merge nem execute pipelines.

SQL é opcional e somente leitura. Antes de qualquer consulta, leia `C:\Users\GabrielLima\.claude\CLAUDE.md` e use somente o mecanismo ali documentado. Para `SELECT` não agregado, use `TOP 1000` e uma janela temporal curta. Nunca solicite, exiba ou armazene credenciais.

## Limites

Não reproduza o BUG, não execute testes ou endpoints para revalidar a correção, não modifique código/branch/PR/Work Item, não proponha solução alternativa ou refatoração não solicitada. Testes e endpoints existentes podem ser lidos apenas como evidência histórica.

Use os subagentes somente quando agregarem valor: `evidence_explorer` coleta fatos, `solution_mapper` conecta plano e implementação, e `learning_assessor` avalia uma resposta. Todos permanecem read-only.

