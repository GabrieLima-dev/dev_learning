# Ensinar e preparar a prática

## Quando a ação for `TEACH`

1. Leia na saída o objetivo, tipo e pré-requisitos da aula.
2. Execute `python3 scripts/learning.py teach`.
3. Apresente, nesta ordem:
   - objetivo observável;
   - explicação curta e adequada ao nível atual;
   - exemplo mínimo que não resolva o exercício;
   - motivo técnico da localização de source e teste.

Para `initial-diagnostic`, não dê aula: prepare de dois a quatro microdesafios independentes sobre fundamentos. O resultado pode marcar como dominadas apenas aulas realmente demonstradas.

Para `checkpoint`, reduza os TODOs e combine conhecimentos já concluídos. Não introduza conceito novo.

Para `git-github-foundations` e `git-github-collaboration`, combine uma alteração pequena compatível com os conhecimentos já adquiridos e uma prática observável no repositório. Explique o efeito de cada comando antes do aluno executá-lo e peça que ele interprete `status`, `diff` ou o histórico; não transforme a aula em uma lista de comandos para decorar. Inclua higiene de segredos e diferencie ações locais de ações que modificam o GitHub.

## Criar o exercício

1. Reuse o domínio e as classes existentes quando isso fizer sentido; não reconstrua o projeto.
2. Crie o starter em `src/main/java/dev/learning/...` com assinatura, tipos e TODOs suficientes, mas sem corpo que entregue a resposta.
3. Crie testes JUnit em `src/test/java/dev/learning/...`. Nomes dos testes devem explicar comportamentos e cobrir os critérios objetivos, sem depender do texto do tutor.
4. Confirme que os arquivos estão dentro do workspace e registre:

```bash
python3 scripts/learning.py assign \
  --name "NomeDoExercicio" \
  --source src/main/java/dev/learning/caminho/Arquivo.java \
  --test src/test/java/dev/learning/caminho/ArquivoTest.java
```

5. Informe o que o aluno deve implementar e como executar os testes. Pare e aguarde; não inicie outra aula.

Se `git-github-foundations` já estiver concluída, relembre que, após a aprovação, o aluno revisará as mudanças e criará um commit coerente. Em checkpoints, avise também que a versão aprovada será sincronizada com o GitHub. Não execute essas ações pelo aluno.

Um teste inicialmente vermelho por TODO é esperado. Erro de compilação intencional não é: o starter deve compilar sempre que a natureza do exercício permitir.
