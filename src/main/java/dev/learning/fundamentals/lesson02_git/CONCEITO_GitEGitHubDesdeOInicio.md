# Git e GitHub desde o início

Git é um sistema de controle de versão. Ele registra versões de arquivos e permite entender o que mudou, quando mudou e qual foi a intenção daquela mudança. O repositório local é a pasta do projeto mais o histórico que o Git guarda nela. GitHub é um serviço remoto para hospedar repositórios Git e colaborar; ele não substitui o Git instalado no computador. Nesta aula, os comandos Git serão executados no terminal integrado do IntelliJ, na raiz do projeto.

O diretório de trabalho (*working tree*) é o estado atual dos arquivos. `git status` mostra o que o Git percebe: arquivos modificados, arquivos novos ainda não rastreados e mudanças que já estão preparadas. Um arquivo rastreado já pertence ao histórico; um arquivo não rastreado ainda não. Para ver a diferença de um arquivo modificado antes de prepará-lo, usamos `git diff`. Arquivos novos aparecem em `git status`, mas não aparecem no `git diff` comum até serem adicionados ao staging.

O staging area é uma seleção explícita do que entrará no próximo commit. `git add caminho/do/arquivo` prepara apenas aquele arquivo; não significa “salvar tudo”. Depois de preparar, `git diff --staged` permite revisar exatamente o conteúdo que será registrado. Um commit é uma fotografia coerente desse conjunto preparado, acompanhada de uma mensagem curta que explica a intenção. O identificador longo de cada commit é o *hash*, e `git log --oneline` mostra uma visão resumida do histórico.

Antes de criar commits, sua identidade precisa estar configurada. Confira com `git config --get user.name` e `git config --get user.email`. Se algum valor não aparecer, configure a identidade global com `git config --global user.name "Seu Nome"` e `git config --global user.email "seu-email@exemplo.com"`. Esses dados identificam a autoria dos commits; use um e-mail que você aceite associar ao seu histórico. Não inclua senhas, tokens ou outros segredos em arquivos nem em mensagens de commit.

O arquivo `.gitignore` diz quais arquivos locais o Git deve ignorar, como artefatos de build, configuração da IDE, arquivos temporários e segredos. Ele não remove um arquivo que já está sendo rastreado, nem protege um segredo que foi adicionado antes: por isso, sempre revise o que será preparado. Nesta prática, não altere o `.gitignore`; apenas confira que `target/`, `.idea/`, `.env` e extensões de chaves estão cobertos.

Uma branch é uma linha de evolução do histórico; a branch principal deste projeto é `main`. Um remoto é outra cópia acessível do repositório. O remoto normalmente chamado `origin` aponta para o GitHub. `git remote -v` mostra os endereços de busca (*fetch*) e envio (*push*). `git fetch` busca referências do remoto sem alterar seus arquivos; `git pull` busca e integra mudanças na sua branch; `git push` envia commits locais para o remoto. Nesta atividade, você precisa explicar a diferença entre esses comandos, mas não deve executar `push` nem qualquer operação que altere o GitHub.

`git init` cria um repositório Git em uma pasta que ainda não tem histórico. `git clone URL` cria uma cópia local de um repositório remoto que já existe. Este projeto já é um repositório com um remoto configurado, então não execute `init` nem `clone` aqui.

Abra [GitWorkspaceMarker.java](./GitWorkspaceMarker.java), substitua `SEU_NOME_AQUI` conforme o TODO e salve. Então, no terminal integrado, execute os comandos abaixo, um de cada vez, observando a saída:

```text
git status
git diff -- src/main/java/dev/learning/fundamentals/lesson02_git/GitWorkspaceMarker.java
git add -- src/main/java/dev/learning/fundamentals/lesson02_git/GitWorkspaceMarker.java src/main/java/dev/learning/fundamentals/lesson02_git/CONCEITO_GitEGitHubDesdeOInicio.md src/test/java/dev/learning/fundamentals/lesson02_git/GitWorkspaceMarkerTest.java
git diff --staged
./mvnw test
git commit -m "Pratica navegacao Git"
git log --oneline -3
git remote -v
git status -sb
```

No Windows, substitua `./mvnw test` por `mvnw.cmd test`. O primeiro `git status` pode mostrar mudanças que já estavam no projeto e não pertencem a esta aula. Não adicione essas mudanças: o `git add` acima lista somente os três arquivos desta prática. Antes de confirmar o commit, use `git diff --staged` para garantir que somente eles estão preparados e que nenhum segredo aparece na saída. Todos os comandos desta prática atuam localmente ou apenas consultam o remoto; não é necessário autenticar no GitHub.

Quando finalizar, informe: o que `git status` mostrou antes e depois do `git add`; por que `git diff --staged` é importante; o hash curto do seu commit; e o que `git push` faria se fosse executado. Você também deve explicar a diferença entre Git e GitHub e entre `pull` e `push`.

Quando terminar a prática, execute `./mvnw test` no macOS ou Linux, ou `mvnw.cmd test` no Windows. Você pode abrir [GitWorkspaceMarkerTest.java](../../../../../../test/java/dev/learning/fundamentals/lesson02_git/GitWorkspaceMarkerTest.java) para consultar o comportamento verificado.
