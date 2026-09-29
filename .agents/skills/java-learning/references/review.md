# Revisar exercício

## Abrir ou retomar

Execute:

```bash
python3 scripts/learning.py review-start
./mvnw test
```

No Windows use `mvnw.cmd test`. Se o estado já for `REVIEWING`, apenas execute novamente os testes e a análise.

## Avaliação combinada

Leia o source ativo, o teste ativo e apenas as classes colaboradoras necessárias. Verifique:

- o comportamento objetivo passou;
- o conceito da aula foi realmente usado, sem contorno;
- a solução não depende de conceito futuro para ser considerada correta;
- feedbacks antigos resolvidos foram removidos.

Em `intellij-idea-foundations`, o source e os testes já começam implementados. Além de executar a suíte, confirme pelo relato do aluno que ele:

- localizou source e teste na árvore do projeto;
- executou pelo gutter ao menos um método de teste e a classe de teste;
- executou no terminal integrado tanto a suíte quanto a classe de teste específica;
- reconheceu onde aparecem sucesso, falha, erro de compilação, mensagem e stack trace;
- sabe que usará o mesmo terminal para os comandos Git da aula seguinte.

Não cobre alteração de código ou conhecimento de sintaxe Java nessa aula.

Em `git-github-foundations`, além do teste e da pequena alteração proposta, confirme pelo relato e pelas saídas apresentadas pelo aluno que ele:

- diferencia Git de GitHub e estado local de estado remoto;
- interpreta `status`, `diff` e `diff --staged`;
- preparou somente os arquivos pertinentes e criou um commit coerente;
- encontrou o commit no histórico e conferiu o remoto configurado;
- sabe explicar o efeito de `pull` e `push` e não expôs credenciais ou artefatos locais.

O aluno executa os comandos. Não faça commit ou push por ele sem pedido explícito.

Classifique pendências em `SYNTAX`, `LOGIC`, `CONCEPT`, `DESIGN` ou `GOOD_PRACTICE`. Só as pendências impeditivas da aula reprovam; não transforme preferências em bloqueios.

Quando a localização ajudar, adicione perto do ponto:

```java
// DEV_LEARNING_FEEDBACK[CONCEPT]: Que estado este método precisa preservar?
```

O comentário deve orientar, não conter a correção. Não modifique nenhuma outra linha da implementação do aluno.

## Resultado

Se requer correção:

```bash
python3 scripts/learning.py review-result \
  --outcome needs-correction \
  --tests-passed false \
  --analysis-passed false \
  --summary "Resumo curto das pendências"
```

Use os valores reais: testes podem estar verdes e análise falsa. Explique uma pendência por vez e aguarde nova tentativa.

Se aprovado, remova primeiro todos os comentários `DEV_LEARNING_FEEDBACK` resolvidos e execute:

```bash
python3 scripts/learning.py review-result \
  --outcome passed \
  --tests-passed true \
  --analysis-passed true \
  --summary "Competência demonstrada"
```

No diagnóstico, acrescente `--mastered id1,id2` somente para fundamentos demonstrados. Informe a aprovação e o próximo ponto, mas não prepare outra aula até o aluno pedir continuidade.

## Prática contínua de Git

Se `git-github-foundations` constar em `completedLessons`, após a aprovação:

1. Mostre ao aluno como conferir `git status` e revisar o `git diff` relacionado à atividade.
2. Oriente-o a selecionar somente os arquivos pertinentes e criar um commit pequeno, com mensagem que explique a mudança.
3. Se a atividade aprovada for um checkpoint, oriente também a sincronização com o GitHub e a confirmação de que a branch remota recebeu o commit.

O aluno executa e interpreta os comandos. Não faça commit, push ou Pull Request por ele sem pedido explícito. Antes de sugerir versionamento, confira se não há credenciais, `.env`, chaves, artefatos de build ou arquivos pessoais da IDE entre as mudanças. Não use comandos destrutivos para “limpar” o repositório.

Na aprovação do projeto final, além dos critérios técnicos, exija um remoto GitHub configurado, branch principal sincronizada, histórico compreensível, `.gitignore` adequado, ausência de segredos, testes verdes e README com instruções reproduzíveis de preparação, execução e teste.
