# Roadmap da trilha Java, arquitetura e microsserviços

Esta trilha transforma em prática progressiva o conteúdo de referência de `java_arquitetura_ms-main`. Java e backend são o eixo central; frontend, QA e infraestrutura entram no nível necessário para construir, integrar, testar e entregar uma aplicação web completa.

| Fase | Conteúdo principal | Resultado esperado |
|---|---|---|
| 1. Fundamentos | diagnóstico, JVM/JDK/JRE, estrutura Java, variáveis, tipos, operadores, entrada/saída, condicionais, loops, arrays e strings | Resolver problemas simples e explicar como um programa Java é compilado e executado. |
| 2. Estrutura do código | métodos, parâmetros, retorno, sobrecarga, varargs, escopo, packages, classes, objetos, construtores e membros `static` | Organizar comportamento e modelar objetos simples. |
| 3. Orientação a Objetos | encapsulamento, herança, polimorfismo, composição, interfaces, classes abstratas, `equals` e `hashCode` | Modelar responsabilidades, identidade e contratos. |
| 4. APIs essenciais | Collections, Generics, Enum, Record, classes seladas, exceptions, Optional, BigDecimal, datas, arquivos, annotations e reflexão | Manipular dados com os principais tipos e APIs da plataforma. |
| 5. Java funcional e moderno | lambdas, interfaces funcionais, Streams, pattern matching, text blocks e imutabilidade | Criar transformações de dados legíveis e idiomáticas. |
| 6. Concorrência | threads, executors, futures, sincronização, tipos atômicos, coleções concorrentes e virtual threads | Executar trabalho concorrente com segurança e critérios claros. |
| 7. SQL e acesso a dados | modelo relacional, JDBC, `DataSource`, pool, prepared statements, CRUD, joins, transações, isolamento, batch, paginação, procedures, BLOBs, migrations e Repository | Implementar persistência relacional segura e testável. |
| 8. Engenharia de software | Maven, Gradle, JUnit, Mockito, Clean Code, refatoração, SOLID, logging e organização por funcionalidade | Produzir código sustentável, testável e bem organizado. |
| 9. Backend com Quarkus | Jakarta EE, Maven multi-módulo, HTTP/REST, JAX-RS, JSON, DTOs, endpoints, CDI, configuração, validação, services, mappers e erros | Construir uma API com contratos e responsabilidades bem separados. |
| 10. Persistência com ORM | JPA, Hibernate, entidades, relacionamentos, queries, identificadores, constraints, transações, Agroal, H2 e múltiplos datasources | Persistir o domínio por ORM sem misturar infraestrutura e regra de negócio. |
| 11. Microsserviços e processamento assíncrono | clientes HTTP, autenticação propagada, timeout, retry, resiliência, idempotência, Kafka, Redis, jobs e filas | Integrar serviços e escolher conscientemente entre fluxos síncronos e assíncronos. |
| 12. Segurança e observabilidade | OAuth 2.0, OpenID Connect, JWT, segredos, OpenAPI, health checks, logs, métricas, traces e auditoria | Proteger e operar uma aplicação observável. |
| 13. Testes e entrega | testes unitários, integração Quarkus, RestAssured, Testcontainers, Postman, JasperReports, Docker, pipeline, SonarQube, Kubernetes e Helm | Validar, empacotar e entregar o backend de forma reproduzível. |
| 14. Integração web e QA | visão de Angular/TypeScript, RxJS, estado, design system, tratamento de erros, Cypress, Appium, BrowserStack e automação com Python | Colaborar com frontend e QA entendendo contratos, camadas e estratégias de teste. |
| 15. Projeto final | API, persistência, integração, mensageria, segurança, observabilidade, testes e deploy | Entregar e explicar um microsserviço completo de ponta a ponta. |

## Princípios da progressão

- Cada fase termina em um checkpoint obrigatório antes da seguinte.
- Os exercícios reutilizam o mesmo domínio quando isso torna a evolução visível.
- Recursos de framework só aparecem depois dos fundamentos equivalentes em Java, HTTP, SQL e testes.
- Abstrações corporativas são estudadas como referência; primeiro são usados os recursos nativos da linguagem e do framework.
- Tecnologias antigas citadas no material servem como contexto, não como recomendação automática para projetos novos.
- Frontend e QA são conteúdos complementares: a cobrança principal continua sendo Java/backend.

O conteúdo detalhado, a ordem exata, os objetivos observáveis e os pré-requisitos estão em `curriculum/java.json`.
