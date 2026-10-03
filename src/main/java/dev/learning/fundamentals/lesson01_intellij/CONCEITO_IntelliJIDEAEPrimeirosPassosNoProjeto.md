# IntelliJ IDEA e primeiros passos no projeto

Uma IDE (Integrated Development Environment, ou ambiente integrado de desenvolvimento) reúne em uma só aplicação as tarefas que usamos para criar software: editar código, navegar pelos arquivos, executar programas, rodar testes e usar um terminal. O IntelliJ IDEA é a IDE que vamos usar na trilha. Ele não substitui o Java nem o Maven: ele organiza e oferece uma interface para trabalhar com essas ferramentas.

Para abrir o projeto, selecione no IntelliJ IDEA a pasta raiz `dev_learning`, que contém `pom.xml` e os arquivos `mvnw` e `mvnw.cmd`. Quando a IDE reconhecer o Maven, aceite a importação e aguarde a indexação e o carregamento das dependências. Confirme também que o projeto utiliza o JDK 25. Se as dependências, os packages ou os ícones de execução não aparecerem corretamente, abra a janela **Maven** e recarregue o projeto.

A janela **Project** mostra a árvore de arquivos. É por ela que você pode chegar rapidamente ao código da prática e aos testes. O **Editor** é a área central onde o arquivo aberto aparece. À esquerda do número de cada linha, a margem chamada **gutter** exibe ícones: em uma classe ou método executável, ela oferece execução; em um teste, permite executar aquele teste ou o conjunto correspondente. A janela **Run**, normalmente exibida na parte inferior, mostra a saída dos programas e, ao executar testes, apresenta a árvore de resultados e o console da sessão. A janela **Terminal** abre uma linha de comando integrada ao projeto.

Este é um projeto Maven. O arquivo `pom.xml` descreve o projeto e suas dependências, incluindo o JUnit, que usamos para testes. `mvnw` é o Maven Wrapper: ele permite chamar a versão preparada para o projeto sem depender de uma instalação global do Maven. No macOS e Linux, o comando da suíte é `./mvnw test`; no Windows, é `mvnw.cmd test`.

Os arquivos de produção ficam em `src/main/java` e os testes ficam em `src/test/java`. Dentro dessas pastas, os diretórios representam o **package**, uma forma de agrupar classes relacionadas. Uma **classe** pode reunir dados e comportamentos; um **método** representa uma operação declarada dentro dela. Nesta prática, `IdeaWorkspaceTour` tem o método `main`, que pode ser executado como programa, e `welcomeMessage`, chamado pelos testes. `IdeaWorkspaceTourTest` é uma classe de testes JUnit: cada método marcado com `@Test` verifica um comportamento esperado.

Comece localizando `IdeaWorkspaceTour.java` pela janela Project. Abra também `IdeaWorkspaceTourTest.java`. Pressione `Shift` duas vezes para abrir o **Search Everywhere**, que encontra arquivos, classes, ações e configurações. Você também pode usar a busca específica de arquivos: no macOS, `⌘⇧O`; no Windows e Linux, `Ctrl+Shift+N`. Para procurar comandos da IDE, use *Find Action*: `⌘⇧A` no macOS ou `Ctrl+Shift+A` no Windows e Linux. Para ir à declaração de algo sob o cursor, use `⌘B` no macOS ou `Ctrl+B` no Windows e Linux.

Execute `IdeaWorkspaceTour.main` pelo ícone verde do gutter ao lado do método. A janela Run deve mostrar a mensagem `Projeto pronto para explorar no IntelliJ IDEA.`. Para parar uma execução que esteja em andamento, use o botão quadrado de parar nessa mesma janela. Você também pode repetir a última execução com `Ctrl+R` no macOS ou `Shift+F10` no Windows e Linux; confirme os atalhos mostrados pela sua instalação, pois keymaps personalizados podem mudá-los.

Agora use o gutter do método `returnsTheMessageShownByTheExampleProgram` para executar somente esse teste. Em seguida, execute o gutter da classe `IdeaWorkspaceTourTest` para rodar seus dois testes. Por fim, execute a suíte completa pela janela Maven da IDE, escolhendo o ciclo `test`, ou pelo terminal integrado. Para abrir o terminal, procure a janela **Terminal** na barra inferior; antes de rodar um comando, observe o diretório exibido no prompt e confirme que ele é a raiz do projeto, onde estão `pom.xml` e `mvnw`.

No terminal integrado, rode a suíte completa com `./mvnw test` no macOS/Linux ou `mvnw.cmd test` no Windows. Para rodar somente a classe de testes desta aula pelo Maven, use `./mvnw -Dtest=IdeaWorkspaceTourTest test` no macOS/Linux ou `mvnw.cmd -Dtest=IdeaWorkspaceTourTest test` no Windows. Os dois comandos usam o Maven; a opção `-Dtest=...` limita a execução a uma classe de teste. Ao executar `IdeaWorkspaceTourTest`, o resumo deve informar 2 testes sem falhas ou erros e terminar com `BUILD SUCCESS`.

Um resultado verde significa que a execução terminou e as verificações esperadas passaram. Uma falha de teste normalmente mostra qual expectativa não foi atendida; ela não é o mesmo que erro de compilação. Um erro de compilação acontece antes de os testes rodarem, quando o código não pode ser preparado pelo Java. Se houver um problema durante uma execução, a mensagem ajuda a localizar a causa, e o **stack trace** mostra a sequência de chamadas que levou até ela. Leia primeiro a mensagem mais clara e, depois, os arquivos e linhas do seu próprio projeto listados no stack trace.

Nesta aula não é preciso escrever Java. O objetivo é ganhar familiaridade com o projeto e com as ferramentas. Siga este checklist:

1. Localize e abra o source e o teste pela janela Project ou pelo Search Everywhere.
2. Execute `IdeaWorkspaceTour.main` pelo gutter e confirme a mensagem na janela Run.
3. Execute somente o método `returnsTheMessageShownByTheExampleProgram` pelo gutter.
4. Execute a classe `IdeaWorkspaceTourTest` pelo gutter e confirme seus 2 testes.
5. Execute a suíte completa pela janela Maven da IDE.
6. Abra o terminal integrado, confirme que ele está na raiz do projeto e execute a suíte completa.
7. Execute somente `IdeaWorkspaceTourTest` pelo Maven usando `-Dtest=IdeaWorkspaceTourTest`.
8. Informe quais ações realizou e como reconheceu um resultado bem-sucedido e uma possível falha.

Na próxima aula, o terminal integrado também será usado para comandos Git.

Agora abra [IdeaWorkspaceTour.java](./IdeaWorkspaceTour.java) e realize os TODOs como checklist.

Quando finalizar, execute `./mvnw test` no macOS ou Linux, ou `mvnw.cmd test` no Windows. Você pode abrir [IdeaWorkspaceTourTest.java](../../../../../../test/java/dev/learning/fundamentals/lesson01_intellij/IdeaWorkspaceTourTest.java) para consultar os comportamentos verificados.
