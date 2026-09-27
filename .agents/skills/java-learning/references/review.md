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
