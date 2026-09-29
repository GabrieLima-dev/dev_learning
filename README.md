# DEV_LEARNING

Trilha prática e cumulativa de Java, arquitetura e microsserviços conduzida pelo Codex. O aprendizado começa nos fundamentos da linguagem e evolui até a construção, os testes e o deploy de um microsserviço completo.

O currículo, o progresso e a avaliação ficam registrados no próprio projeto. Assim, uma nova sessão continua exatamente do ponto anterior, preservando exercícios, revisões e resultados. Java e backend são o eixo principal; frontend, QA e infraestrutura aparecem como conhecimentos complementares para compreender a aplicação de ponta a ponta.

## O que você vai aprender

A trilha possui 15 fases, 14 checkpoints obrigatórios e um projeto final:

| Fase | Assuntos principais |
|---|---|
| 1. Fundamentos | IntelliJ IDEA, organização do projeto, execução de classes e testes, terminal integrado, Git e GitHub, JVM, JDK, JRE, estrutura Java, tipos, operadores, entrada e saída, condicionais, loops, arrays e strings. |
| 2. Estrutura do código | Métodos, parâmetros, retornos, sobrecarga, varargs, escopo, packages, classes, objetos e membros `static`. |
| 3. Orientação a Objetos | Encapsulamento, herança, polimorfismo, composição, interfaces, classes abstratas, `equals` e `hashCode`. |
| 4. APIs essenciais | Collections, Generics, Enum, Record, classes seladas, exceptions, Optional, BigDecimal, datas, arquivos e annotations. |
| 5. Java funcional e moderno | Lambdas, interfaces funcionais, Streams, pattern matching, text blocks e imutabilidade. |
| 6. Concorrência | Threads, executors, futures, sincronização, tipos atômicos, coleções concorrentes e virtual threads. |
| 7. SQL e acesso a dados | Modelo relacional, JDBC, pool de conexões, CRUD, joins, transações, batch, paginação, migrations e Repository. |
| 8. Engenharia de software | Maven, Gradle, branches e colaboração com Git/GitHub, IntelliJ IDEA, JUnit, Mockito, bugs, PBIs, debugger, investigação de causa raiz, Clean Code, refatoração, SOLID e logging. |
| 9. Backend com Quarkus | Jakarta EE, HTTP/REST, JAX-RS, JSON, DTOs, CDI, configuração, validação, services, mappers e tratamento de erros. |
| 10. Persistência com ORM | JPA, Hibernate, entidades, relacionamentos, queries, constraints, transações e datasources. |
| 11. Microsserviços | Clientes HTTP, resiliência, idempotência, Kafka, Redis, jobs e processamento assíncrono. |
| 12. Segurança e observabilidade | OAuth 2.0, OpenID Connect, JWT, segredos, OpenAPI, health checks, logs, métricas, traces e auditoria. |
| 13. Testes e entrega | RestAssured, Testcontainers, Postman, JasperReports, Docker, pipelines, SonarQube, Kubernetes e Helm. |
| 14. Integração web e QA | Angular, TypeScript, RxJS, estado, design system, Cypress, Appium, BrowserStack e automação com Python. |
| 15. Projeto final | Construção, proteção, observação, teste, empacotamento e publicação documentada de um microsserviço completo em um repositório GitHub atualizado. |

Cada fase termina com uma prática que verifica se os conceitos foram realmente aplicados. A ordem detalhada, os objetivos e os pré-requisitos estão no [currículo](curriculum/java.json), enquanto o [roadmap](docs/roadmap.md) apresenta a visão geral da progressão.

## Como usar este repositório como template

Cada aluno deve criar o próprio repositório a partir deste template. Assim, o progresso, os exercícios e o histórico Git ficam separados da versão original da trilha, e o aluno pode fazer commits e pushes desde o início.

### 1. Criar seu repositório

1. No topo desta página, clique em **Use this template**.
2. Selecione **Create a new repository**.
3. Escolha sua conta como proprietária, defina um nome e selecione visibilidade pública ou privada.
4. Clique em **Create repository from template**.

Use o template em vez de clonar diretamente este repositório. Um clone direto mantém o `origin` apontando para o projeto original, no qual o aluno não possui permissão de escrita. O repositório criado pelo template já pertence ao aluno e começa com seu próprio histórico.

### 2. Clonar sua cópia

Copie a URL do repositório recém-criado e execute:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 3. Conferir o ambiente

É necessário ter Git, Java 25 e Python 3.10 ou superior. O Maven não precisa ser instalado separadamente porque o projeto inclui o Maven Wrapper.

No Linux ou macOS:

```bash
java --version
python3 --version
./mvnw test
python3 scripts/validate.py
```

No Windows:

```powershell
java --version
py -3 --version
mvnw.cmd test
py -3 scripts/validate.py
```

Todos os checks devem passar antes do início da trilha. Se o sistema negar permissão para executar o Maven Wrapper no Linux ou macOS, execute uma vez `chmod +x mvnw` e repita a validação.

### 4. Iniciar a trilha

Abra a pasta clonada no IntelliJ IDEA e no Codex. No Codex, diga:

```text
vamos começar o aprendizado de Java
```

O Codex lerá as regras em `AGENTS.md`, usará a skill `java-learning` e continuará sempre pelo estado registrado em `.learning/progress.json`. Cada aluno deve trabalhar somente em sua própria cópia; este repositório permanece como o template limpo da trilha.

## IntelliJ IDEA desde o início

Depois do diagnóstico opcional, a primeira aula regular apresenta o IntelliJ IDEA antes de Git e dos fundamentos de Java. O aluno aprende o que é uma IDE, reconhece as áreas principais da interface e entende a organização do projeto Maven: `pom.xml`, Maven Wrapper, `src/main/java`, `src/test/java`, packages, classes, métodos e testes.

A prática mostra como localizar arquivos e ações, executar e interromper uma classe, rodar um método de teste, uma classe de teste e a suíte completa, além de interpretar sucesso, falha, erro de compilação e stack trace. O aluno também usa o terminal integrado para executar o Maven Wrapper e aprende a rodar somente o arquivo de teste da aula. Esse mesmo terminal será usado em seguida para Git.

## Git e GitHub desde o início

Git fará parte da rotina desde o começo da trilha, logo após a aula inicial do IntelliJ IDEA. **Git** é o sistema de controle de versão que registra a evolução local dos arquivos; **GitHub** é a plataforma remota onde o repositório pode ser armazenado, sincronizado e compartilhado. A aula apresenta o fluxo entre diretório de trabalho, área de preparação (*staging*) e histórico do repositório.

O aluno aprenderá gradualmente a:

- inspecionar alterações com `git status` e `git diff`;
- selecionar mudanças com `git add` e criar commits pequenos e claros com `git commit`;
- consultar o histórico com `git log` e comparar versões;
- desfazer alterações com segurança, entendendo antes o que será descartado;
- configurar `.gitignore` e nunca versionar senhas, tokens, chaves, arquivos `.env`, caches ou artefatos de build;
- conectar o repositório local ao GitHub e sincronizá-lo com `git pull` e `git push`;
- trabalhar com branches usando `git switch`, integrar mudanças e resolver conflitos conscientemente;
- revisar diferenças, usar Pull Requests e marcar versões relevantes do projeto.

Depois que esses fundamentos forem apresentados, cada exercício aprovado também incluirá a revisão do diff e um commit coerente. Os checkpoints serão enviados ao GitHub para manter uma cópia remota atualizada. O tutor orientará os comandos e explicará o efeito de cada um; operações que possam apagar trabalho não serão tratadas como atalhos comuns.

Ao final da trilha, o projeto final deverá estar em um repositório GitHub público ou privado do aluno, com a branch principal sincronizada, histórico compreensível, `.gitignore` adequado, nenhuma credencial versionada, testes passando e um README que explique como preparar, executar e testar a aplicação.

## IntelliJ IDEA avançado, bugs e investigação

Na fase de Engenharia de software, a trilha aprofunda o IntelliJ IDEA depois que o aluno já domina o fluxo básico. A prática inclui navegar por declarações, implementações e usos, criar configurações de Run/Debug, usar breakpoints e inspeções, gerar e formatar código e aplicar refatorações seguras com pré-visualização.

Um **bug** é um comportamento observável diferente do esperado. Um **PBI** (*Product Backlog Item*) é um item priorizado do backlog que descreve valor, necessidade ou trabalho a realizar; ele pode representar uma funcionalidade, uma melhoria, uma pesquisa técnica ou até a correção de um bug. Para evitar confundir sintoma com causa, cada item será estudado com contexto, comportamento esperado, comportamento atual, passos de reprodução, evidências e critérios de aceite.

A investigação de um bug seguirá um processo reproduzível:

1. Entender o relato e definir claramente o resultado esperado e o resultado atual.
2. Reproduzir a falha no menor cenário possível e registrar dados, ambiente e passos usados.
3. Ler mensagens de erro, stack traces, logs e testes antes de alterar o código.
4. Formular hipóteses e acompanhar o fluxo com breakpoints, execução passo a passo, pilha de chamadas, variáveis, watches, avaliação de expressões e breakpoints condicionais ou logpoints.
5. Localizar a causa raiz, distinguindo-a do ponto onde o sintoma apareceu.
6. Criar um teste que falhe pelo motivo correto, quando o caso puder ser automatizado.
7. Fazer a menor correção coerente e verificar efeitos colaterais.
8. Executar o teste de regressão e a suíte relacionada, conferir os critérios de aceite e registrar a evidência da correção.

O objetivo não é decorar todos os atalhos da IDE, mas aprender a encontrar comandos e usar as ferramentas certas para navegar, executar, observar e validar o software com autonomia.

## Começar

Abra esta pasta no Codex e diga:

```text
vamos começar o aprendizado de Java
```

Depois, use linguagem natural:

- `vamos continuar o aprendizado`
- `terminei`
- `resumo da última aula`
- `quero revisar collections`

O Codex lê [AGENTS.md](AGENTS.md), aciona a skill `java-learning` e usa o controlador de estado. Não é necessário memorizar comandos.

## Como funciona a aprendizagem

```text
READY → TEACHING → WAITING_FOR_STUDENT → REVIEWING
                                      ↘ NEEDS_CORRECTION → WAITING_FOR_STUDENT
                                      ↘ PASSED → COMPLETED → READY
```

- `curriculum/java.json`: módulos, ordem, objetivos, checkpoints e pré-requisitos da trilha.
- `.learning/progress.json`: posição e exercício ativo.
- `.learning/session.md`: resumo curto da última sessão.
- `.learning/history.md`: transições para recuperação entre sessões.
- `src/main/java`: implementação do aluno.
- `src/test/java`: critérios objetivos em JUnit.
- `scripts/learning.py`: máquina de estados determinística.
- `.agents/skills/java-learning`: fluxo pedagógico do Codex.

Currículo, estado e avaliação permanecem separados. Em cada aula, o Codex apresenta o objetivo e uma explicação curta, prepara a estrutura inicial e aguarda o aluno programar. Os testes guardam os critérios objetivos; não há arquivo de metadata paralelo para cada exercício.

## Ferramentas para diagnóstico

Os comandos abaixo são úteis para manutenção; durante a aula o Codex os executa:

```bash
python3 scripts/learning.py status
python3 scripts/learning.py continue
python3 scripts/learning.py summary
python3 scripts/validate.py
./mvnw test
```

No Windows, substitua `python3` por `py -3` quando necessário e use `mvnw.cmd test`.

## Avaliação

Uma atividade só passa quando os testes JUnit passam, a análise confirma o uso do conceito ensinado e não restam marcadores `DEV_LEARNING_FEEDBACK`.

Se houver pendência, o Codex classifica o problema, comenta de forma temporária próximo ao código e aguarda nova tentativa sem sobrescrever a solução.

## Ambiente

- Java 25
- Maven 3.9.16 via wrapper
- JUnit 6.1.3
- Python 3.10+ apenas para o controlador local

## Licença

Este projeto utiliza a [DEV_LEARNING Mixed License 1.0](LICENSE.md), registrada em nome de Gabriel de Souza Lima.

- A **área de trabalho do aluno** pode ser usada, modificada e redistribuída sob os termos permissivos descritos na licença. Ela inclui código da aplicação, testes do aluno, progresso, configurações, infraestrutura e o README do projeto final.
- O **núcleo protegido** inclui currículo, regras e skill do agente, controlador de aprendizagem, documentação pedagógica, avaliações e testes do controlador.
- O núcleo protegido pode ser copiado, usado e redistribuído, inclusive comercialmente, desde que permaneça sem alterações, preserve a atribuição e inclua a licença.
- Uma cópia pode conter o núcleo protegido intacto junto com exercícios e projeto final modificados pelo aluno.
- Versões modificadas do núcleo protegido não podem ser publicadas ou redistribuídas sem autorização prévia e escrita do titular.

Esta é uma licença personalizada de código-fonte disponível (*source-available*), não uma licença open source reconhecida pela Open Source Initiative. O texto completo e a definição exata dos caminhos estão em [LICENSE.md](LICENSE.md).

Veja [docs/architecture.md](docs/architecture.md), [docs/roadmap.md](docs/roadmap.md) e [docs/traceability.md](docs/traceability.md).
