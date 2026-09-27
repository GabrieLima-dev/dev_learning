# DEV_LEARNING

Trilha prática e cumulativa de Java, arquitetura e microsserviços conduzida pelo Codex. O aprendizado começa nos fundamentos da linguagem e evolui até a construção, os testes e o deploy de um microsserviço completo.

O currículo, o progresso e a avaliação ficam registrados no próprio projeto. Assim, uma nova sessão continua exatamente do ponto anterior, preservando exercícios, revisões e resultados. Java e backend são o eixo principal; frontend, QA e infraestrutura aparecem como conhecimentos complementares para compreender a aplicação de ponta a ponta.

## O que você vai aprender

A trilha possui 15 fases, 14 checkpoints obrigatórios e um projeto final:

| Fase | Assuntos principais |
|---|---|
| 1. Fundamentos | JVM, JDK, JRE, estrutura Java, tipos, operadores, entrada e saída, condicionais, loops, arrays e strings. |
| 2. Estrutura do código | Métodos, parâmetros, retornos, sobrecarga, varargs, escopo, packages, classes, objetos e membros `static`. |
| 3. Orientação a Objetos | Encapsulamento, herança, polimorfismo, composição, interfaces, classes abstratas, `equals` e `hashCode`. |
| 4. APIs essenciais | Collections, Generics, Enum, Record, classes seladas, exceptions, Optional, BigDecimal, datas, arquivos e annotations. |
| 5. Java funcional e moderno | Lambdas, interfaces funcionais, Streams, pattern matching, text blocks e imutabilidade. |
| 6. Concorrência | Threads, executors, futures, sincronização, tipos atômicos, coleções concorrentes e virtual threads. |
| 7. SQL e acesso a dados | Modelo relacional, JDBC, pool de conexões, CRUD, joins, transações, batch, paginação, migrations e Repository. |
| 8. Engenharia de software | Maven, Gradle, JUnit, Mockito, Clean Code, refatoração, SOLID, logging e organização por funcionalidade. |
| 9. Backend com Quarkus | Jakarta EE, HTTP/REST, JAX-RS, JSON, DTOs, CDI, configuração, validação, services, mappers e tratamento de erros. |
| 10. Persistência com ORM | JPA, Hibernate, entidades, relacionamentos, queries, constraints, transações e datasources. |
| 11. Microsserviços | Clientes HTTP, resiliência, idempotência, Kafka, Redis, jobs e processamento assíncrono. |
| 12. Segurança e observabilidade | OAuth 2.0, OpenID Connect, JWT, segredos, OpenAPI, health checks, logs, métricas, traces e auditoria. |
| 13. Testes e entrega | RestAssured, Testcontainers, Postman, JasperReports, Docker, pipelines, SonarQube, Kubernetes e Helm. |
| 14. Integração web e QA | Angular, TypeScript, RxJS, estado, design system, Cypress, Appium, BrowserStack e automação com Python. |
| 15. Projeto final | Construção, proteção, observação, teste, empacotamento e explicação de um microsserviço completo. |

Cada fase termina com uma prática que verifica se os conceitos foram realmente aplicados. A ordem detalhada, os objetivos e os pré-requisitos estão no [currículo](curriculum/java.json), enquanto o [roadmap](docs/roadmap.md) apresenta a visão geral da progressão.

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
