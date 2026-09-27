# DEV_LEARNING

Trilha prática e cumulativa de Java, arquitetura e microsserviços conduzida pelo Codex. O aprendizado começa nos fundamentos da linguagem e evolui até a construção, os testes e o deploy de um microsserviço completo.

O currículo, o progresso e a avaliação ficam registrados no próprio projeto. Assim, uma nova sessão continua exatamente do ponto anterior, preservando exercícios, revisões e resultados. Java e backend são o eixo principal; frontend, QA e infraestrutura aparecem como conhecimentos complementares para compreender a aplicação de ponta a ponta.

## O que você vai aprender

A trilha possui 15 fases, 14 checkpoints obrigatórios e um projeto final:

| Fase | Assuntos principais |
|---|---|
| 1. Fundamentos | Git e GitHub, JVM, JDK, JRE, estrutura Java, tipos, operadores, entrada e saída, condicionais, loops, arrays e strings. |
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

## Git e GitHub desde o início

Git fará parte da rotina desde a primeira atividade. **Git** é o sistema de controle de versão que registra a evolução local dos arquivos; **GitHub** é a plataforma remota onde o repositório pode ser armazenado, sincronizado e compartilhado. A primeira aula após o diagnóstico apresenta o fluxo entre diretório de trabalho, área de preparação (*staging*) e histórico do repositório.

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

## IntelliJ IDEA, bugs e investigação

Na fase de Engenharia de software, a trilha também ensina a usar o IntelliJ IDEA como ferramenta de trabalho. A prática inclui abrir e importar projetos Maven, reconhecer a estrutura do projeto, navegar entre classes e usos, buscar arquivos, símbolos e ações, executar aplicações e testes, criar configurações de execução e depuração, usar o terminal integrado e aplicar com segurança recursos de geração de código e refatoração.

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

Veja [docs/architecture.md](docs/architecture.md), [docs/roadmap.md](docs/roadmap.md) e [docs/traceability.md](docs/traceability.md).
