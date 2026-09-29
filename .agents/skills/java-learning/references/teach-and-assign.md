# Ensinar e preparar a prática

## Quando a ação for `TEACH`

1. Leia na saída o objetivo, tipo e pré-requisitos da aula.
2. Execute `python3 scripts/learning.py teach`.
3. Prepare o material conceitual, o starter e os testes conforme a seção “Criar o exercício”. Não apresente a explicação da aula diretamente no chat.

Para `initial-diagnostic`, prepare de dois a quatro microdesafios independentes sobre fundamentos. No `CONCEITO.md`, explique que o diagnóstico serve apenas para identificar o ponto inicial, é opcional e pode ser pulado escrevendo esse pedido no chat. O resultado pode marcar como dominadas apenas aulas realmente demonstradas.

Se o aluno pedir para pular, não revise a solução, não peça correções e não exija que os testes passem. Execute:

```bash
python3 scripts/learning.py skip-diagnostic
```

Esse comando só funciona no `initial-diagnostic`. Ele registra a escolha, arquiva os arquivos já criados acrescentando o sufixo `.skipped` para que não interfiram nos próximos testes e leva o aluno à primeira aula regular definida no currículo. Explique que nenhuma aula posterior será marcada como dominada ou ignorada: o aluno seguirá a trilha completa a partir dessa primeira aula.

Para `checkpoint`, reduza os TODOs e combine conhecimentos já concluídos. Não introduza conceito novo.

Para `intellij-idea-foundations`, prepare uma introdução completa para quem nunca usou uma IDE. O `CONCEITO.md` deve explicar:

- o que é uma IDE e o que o IntelliJ IDEA integra;
- as áreas Project, Editor, gutter, Run, Test Results e Terminal;
- a organização do projeto, incluindo `pom.xml`, Maven Wrapper, `src/main/java`, `src/test/java`, package, classe, método e teste;
- as ações e os atalhos básicos para buscar arquivos e ações, abrir declarações, executar, interromper e repetir uma execução, citando as diferenças entre macOS, Linux e Windows quando necessário;
- como executar uma classe, um método de teste, uma classe de teste e a suíte completa pela interface;
- como abrir o terminal integrado, reconhecer o diretório atual e executar `./mvnw test` ou `mvnw.cmd test`;
- como executar apenas a classe de teste da aula pelo Maven e interpretar sucesso, falha, erro de compilação, mensagem e stack trace;
- que o terminal integrado será usado na aula seguinte para os comandos Git.

A prática deve permitir que o aluno localize o Java e o teste pela árvore do projeto, execute um teste pelo gutter e pelo terminal, execute a suíte completa e relate a diferença entre um resultado verde e uma falha. Não pressuponha conhecimento prévio do IntelliJ, Maven ou da estrutura Java.

Essa aula é operacional e acontece antes do ensino de Java. Portanto:

- entregue um source mínimo e testes simples já implementados, compilando e passando desde o início;
- use TODOs em comentários como checklist das ações que o aluno realizará na IDE e no terminal, sem pedir que ele escreva sintaxe Java;
- inclua no `CONCEITO.md` o comando para a suíte e o comando Maven com `-Dtest=NomeDaClasseTest` para executar somente a classe de teste criada;
- peça que o aluno informe quais ações executou e como reconheceu o resultado de sucesso;
- avalie o uso das ferramentas e a interpretação da saída, não uma implementação Java.

Para `git-github-foundations`, escreva o `CONCEITO.md` para quem nunca usou controle de versão. A explicação deve construir uma visão completa e progressiva:

- apresente o problema que o controle de versão resolve e diferencie claramente Git, que registra versões localmente, de GitHub, que hospeda e compartilha repositórios remotos;
- explique repositório, diretório de trabalho, arquivo não rastreado ou modificado, staging area, commit, hash, histórico, branch principal, remoto e `origin`;
- mostre o fluxo mental `alterar → inspecionar → preparar → conferir → registrar → sincronizar`, explicando por que cada etapa existe;
- diferencie `git init` de `git clone` e esclareça que uma cópia criada deste template já é um repositório, portanto não deve ser inicializada novamente;
- explique a configuração de identidade com `user.name` e `user.email`, deixando claro o alcance de `--global` e que esses valores identificam a autoria dos commits;
- ensine, na ordem em que serão usados, `git status`, `git diff`, `git add <arquivo>`, `git diff --staged`, `git commit`, `git log`, `git remote -v`, `git pull` e `git push`;
- para cada comando, informe o que ele lê ou modifica, se o efeito é local ou remoto e o que o aluno deve observar na saída;
- explique a função de `.gitignore` e proíba o versionamento de senhas, tokens, chaves, `.env`, configurações pessoais da IDE, caches e artefatos de build;
- apresente no GitHub os conceitos de conta, repositório remoto, URL HTTPS ou SSH, autenticação segura e branch principal, sem pedir que credenciais sejam colocadas em comandos, código ou arquivos versionados;
- mostre que `pull` traz e integra mudanças do remoto, enquanto `push` publica commits locais, e que sincronizar não substitui revisar `status`, `diff` e os commits;
- deixe branches de trabalho, merge, rebase, conflitos e Pull Requests para `git-github-collaboration`.

A prática deve combinar uma alteração pequena nos arquivos da aula com um fluxo Git observável no terminal integrado do IntelliJ. Antes de cada comando, explique seu efeito; depois, peça que o aluno interprete a saída. Oriente o uso de `git add` com caminhos específicos, nunca `git add .` como atalho automático. O aluno deve revisar o diff normal e o staged, criar um commit coerente, localizá-lo no histórico, conferir o remoto e executar a sincronização com o GitHub quando o remoto e a autenticação estiverem configurados. O tutor não executa commit ou push pelo aluno.

Para `git-github-collaboration`, combine uma alteração pequena compatível com os conhecimentos já adquiridos e uma prática observável no repositório. Explique o efeito de cada comando antes do aluno executá-lo e peça que ele interprete `status`, `diff` ou o histórico; não transforme a aula em uma lista de comandos para decorar. Inclua higiene de segredos e diferencie ações locais de ações que modificam o GitHub.

## Criar o exercício

1. Reuse o domínio e as classes existentes quando isso fizer sentido; não reconstrua o projeto.
2. Use uma pasta própria para a aula dentro de `src/main/java/dev/learning/...`, com o nome `lessonNN_nome_da_aula`, que seja também um identificador Java válido. `NN` é a posição entre as aulas regulares, com pelo menos dois dígitos; as duas primeiras são `lesson01_intellij` e `lesson02_git`. O diagnóstico inicial usa `lesson00_diagnostico_inicial`. O nome padrão deriva do `id` da aula com hífens trocados por `_`, salvo `directoryName` definido no currículo. Espelhe exatamente esse nome na pasta correspondente em `src/test/java` e no último segmento do `package`. Nessa pasta, crie `CONCEITO_NomeDaAula.md`, usando o título em PascalCase, sem acentos ou símbolos, com estrutura simples e conteúdo completo, adequado ao nível atual.

   O número organiza os arquivos da trilha; o `package` declarado no Java continua usando somente identificadores Java válidos e nomes semânticos, sem segmentos iniciados por número. Como o diretório da aula é uma camada de organização didática, não o copie literalmente para o `package`.

   O `assign` valida esse formato. Ao criar a aula, inclua os diretórios de módulo e domínio que fizerem sentido antes da pasta numerada. Dentro dela:

   - um único cabeçalho principal com o nome da aula;
   - logo abaixo, a explicação do assunto em uma sequência natural de parágrafos;
   - cubra definição, finalidade, funcionamento, termos e regras importantes para compreender o conceito;
   - inclua exemplos diferentes da prática proposta e alertas sobre erros comuns quando forem relevantes;
   - ao final, inclua um link relativo para o source Java da aula;
   - logo depois, oriente o aluno a executar os testes quando terminar e inclua um link relativo para o arquivo JUnit correspondente.

   Modelo:

   ```markdown
   # Condicionais

   Condicionais permitem que um programa escolha comportamentos diferentes
   de acordo com uma situação verdadeira ou falsa. A explicação continua aqui
   até cobrir completamente o conceito necessário para a aula, com exemplos
   diferentes do exercício.

   Agora abra [DecisionExercise.java](./DecisionExercise.java) e realize os TODOs.

   Quando finalizar, execute `./mvnw test` no Linux ou macOS, ou
   `mvnw.cmd test` no Windows. Você pode abrir
   [DecisionExerciseTest.java](../../../../../test/java/dev/learning/conditionals/DecisionExerciseTest.java)
   para consultar os comportamentos verificados.
   ```

   A simplicidade se aplica à estrutura visual, não à profundidade da explicação. Não resuma a ponto de omitir conhecimento necessário para a prática. Também não coloque a solução, o algoritmo do exercício ou conceitos de aulas futuras nesse material.
3. Crie o starter Java na mesma pasta do `CONCEITO_NomeDaAula.md`, com assinaturas e tipos suficientes para orientar o aluno, mas sem corpo que entregue a resposta. O Java deve conter apenas a estrutura da prática e seus TODOs, sem repetir a explicação conceitual.
4. Coloque um TODO em cada ponto que exige implementação. O comentário deve ser suficiente para o aluno entender a prática sem precisar deduzir o requisito pelos testes.

   - Diga o que deve ser produzido a partir dos parâmetros ou do estado disponível.
   - Descreva o resultado que o método, objeto ou fluxo deve apresentar.
   - Informe regras, limites e casos especiais relevantes para aquele ponto.
   - Use os nomes do domínio e distribua a orientação em duas a quatro linhas quando uma frase não for suficiente.
   - Não revele operadores, estruturas de controle, chamadas ou uma sequência de passos que componha a solução.
   - Evite textos vagos, como `implemente aqui` ou `use os parâmetros`.

   Exemplo:

   ```java
   // TODO: calcule o valor total da compra a partir dos preços recebidos.
   // Resultado esperado: devolva a soma dos preços ou zero quando não houver itens.
   // A lista recebida deve permanecer inalterada.
   ```

5. Crie testes JUnit em `src/test/java/dev/learning/...`, espelhando a pasta `NN.id-da-aula` usada pelo source. Nomes dos testes devem explicar comportamentos e cobrir os critérios objetivos, sem depender do texto do tutor. Calcule, a partir do `CONCEITO_NomeDaAula.md`, o link relativo real para esse arquivo e use-o na orientação final da prática.
6. Confirme que `CONCEITO_NomeDaAula.md`, source e teste estão dentro do workspace e registre:

```bash
python3 scripts/learning.py assign \
  --name "NomeDoExercicio" \
  --source src/main/java/dev/learning/caminho/Arquivo.java \
  --test src/test/java/dev/learning/caminho/ArquivoTest.java
```

7. Depois do registro, responda somente com “Vamos começar a nossa aula” e um link absoluto clicável para o material conceitual. O próprio material direcionará o aluno ao Java. Pare e aguarde; não inicie outra aula.

Ao retomar uma aula, responda somente com “Vamos continuar nossa aula” e o link absoluto clicável do material conceitual registrado em `exercise.concept`. Para um exercício antigo sem esse campo, crie `CONCEITO_NomeDaAula.md` ao lado do source ativo e use esse caminho, sem editar `.learning/progress.json` manualmente.

Se `git-github-foundations` já estiver concluída, relembre que, após a aprovação, o aluno revisará as mudanças e criará um commit coerente. Em checkpoints, avise também que a versão aprovada será sincronizada com o GitHub. Não execute essas ações pelo aluno.

Um teste inicialmente vermelho por TODO é esperado. Erro de compilação intencional não é: o starter deve compilar sempre que a natureza do exercício permitir.
