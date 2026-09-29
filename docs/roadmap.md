# Roadmap da trilha Java, arquitetura e microsserviços

Esta trilha transforma em prática progressiva o conteúdo de referência de `java_arquitetura_ms-main`. Java e backend são o eixo central; frontend, QA e infraestrutura entram no nível necessário para construir, integrar, testar e entregar uma aplicação web completa.

| Fase | Conteúdo principal | Resultado esperado |
|---|---|---|
| 1. Fundamentos | diagnóstico, IntelliJ IDEA, organização do projeto, execução de testes, terminal integrado, Git e GitHub, JVM/JDK/JRE, estrutura Java, variáveis, tipos, operadores, entrada/saída, condicionais, loops, arrays e strings | Usar a IDE e os testes com autonomia, versionar a própria evolução, resolver problemas simples e explicar como um programa Java é compilado e executado. |
| 2. Estrutura do código | métodos, parâmetros, retorno, sobrecarga, varargs, escopo, packages, classes, objetos, construtores e membros `static` | Organizar comportamento e modelar objetos simples. |
| 3. Orientação a Objetos | encapsulamento, herança, polimorfismo, composição, interfaces, classes abstratas, `equals` e `hashCode` | Modelar responsabilidades, identidade e contratos. |
| 4. APIs essenciais | Collections, Generics, Enum, Record, classes seladas, exceptions, Optional, BigDecimal, datas, arquivos, annotations e reflexão | Manipular dados com os principais tipos e APIs da plataforma. |
| 5. Java funcional e moderno | lambdas, interfaces funcionais, Streams, pattern matching, text blocks e imutabilidade | Criar transformações de dados legíveis e idiomáticas. |
| 6. Concorrência | threads, executors, futures, sincronização, tipos atômicos, coleções concorrentes e virtual threads | Executar trabalho concorrente com segurança e critérios claros. |
| 7. SQL e acesso a dados | modelo relacional, JDBC, `DataSource`, pool, prepared statements, CRUD, joins, transações, isolamento, batch, paginação, procedures, BLOBs, migrations e Repository | Implementar persistência relacional segura e testável. |
| 8. Engenharia de software | Maven, Gradle, branches e colaboração com Git/GitHub, IntelliJ IDEA, JUnit, Mockito, bugs, PBIs, debugger, investigação de causa raiz, Clean Code, refatoração, SOLID, logging e organização por funcionalidade | Desenvolver, colaborar e corrigir código de modo sustentável, reproduzível, testável e bem organizado. |
| 9. Backend com Quarkus | Jakarta EE, Maven multi-módulo, HTTP/REST, JAX-RS, JSON, DTOs, endpoints, CDI, configuração, validação, services, mappers e erros | Construir uma API com contratos e responsabilidades bem separados. |
| 10. Persistência com ORM | JPA, Hibernate, entidades, relacionamentos, queries, identificadores, constraints, transações, Agroal, H2 e múltiplos datasources | Persistir o domínio por ORM sem misturar infraestrutura e regra de negócio. |
| 11. Microsserviços e processamento assíncrono | clientes HTTP, autenticação propagada, timeout, retry, resiliência, idempotência, Kafka, Redis, jobs e filas | Integrar serviços e escolher conscientemente entre fluxos síncronos e assíncronos. |
| 12. Segurança e observabilidade | OAuth 2.0, OpenID Connect, JWT, segredos, OpenAPI, health checks, logs, métricas, traces e auditoria | Proteger e operar uma aplicação observável. |
| 13. Testes e entrega | testes unitários, integração Quarkus, RestAssured, Testcontainers, Postman, JasperReports, Docker, pipeline, SonarQube, Kubernetes e Helm | Validar, empacotar e entregar o backend de forma reproduzível. |
| 14. Integração web e QA | visão de Angular/TypeScript, RxJS, estado, design system, tratamento de erros, Cypress, Appium, BrowserStack e automação com Python | Colaborar com frontend e QA entendendo contratos, camadas e estratégias de teste. |
| 15. Projeto final | API, persistência, integração, mensageria, segurança, observabilidade, testes, deploy e publicação no GitHub | Entregar e explicar um microsserviço completo de ponta a ponta em um repositório GitHub atualizado e reproduzível. |

## Princípios da progressão

- Cada fase termina em um checkpoint obrigatório antes da seguinte.
- Os exercícios reutilizam o mesmo domínio quando isso torna a evolução visível.
- Recursos de framework só aparecem depois dos fundamentos equivalentes em Java, HTTP, SQL e testes.
- Abstrações corporativas são estudadas como referência; primeiro são usados os recursos nativos da linguagem e do framework.
- Tecnologias antigas citadas no material servem como contexto, não como recomendação automática para projetos novos.
- Frontend e QA são conteúdos complementares: a cobrança principal continua sendo Java/backend.
- A primeira aula regular ensina o fluxo básico do IntelliJ IDEA e a leitura dos testes antes de introduzir Git ou fundamentos de Java.
- Git é uma prática transversal: depois da aula inicial, toda atividade aprovada termina com revisão das mudanças e commit; cada checkpoint inclui sincronização com o GitHub.

## Progressão de Git e GitHub

O versionamento acompanha o código em três níveis:

1. **Início da trilha** — compreender repositório, diretório de trabalho, staging e commit; usar `status`, `diff`, `add`, `commit` e `log`; configurar identidade e `.gitignore`; reconhecer arquivos que não devem ser versionados; conectar o remoto e fazer o primeiro push ao GitHub.
2. **Prática contínua** — revisar o diff antes de cada commit, escrever mensagens que expliquem a mudança, manter commits pequenos, sincronizar checkpoints e confirmar que testes e estado do repositório estão limpos. Nenhum segredo, cache, configuração pessoal da IDE ou artefato de build deve entrar no histórico.
3. **Engenharia e colaboração** — criar e trocar branches, comparar históricos, integrar mudanças, compreender merge e rebase, resolver conflitos, revisar Pull Requests e identificar quando usar tags ou releases.

O projeto final exige um repositório GitHub público ou privado do aluno com a branch principal sincronizada, histórico coerente, `.gitignore` adequado, ausência de credenciais, suíte de testes verde e README com instruções reproduzíveis de preparação, execução e teste.

## Ferramentas e investigação na fase 8

A fase de Engenharia de software inclui três etapas práticas adicionais:

1. **Produtividade avançada com IntelliJ IDEA** — aprofundar a base apresentada no início da trilha; navegar por declarações, implementações e usos; pesquisar símbolos e ações; criar configurações Run/Debug; usar breakpoints e inspeções; gerar código; formatar; renomear e refatorar com pré-visualização.
2. **Bugs, PBIs e critérios de aceite** — diferenciar defeito, sintoma e causa; entender um PBI como item priorizado de trabalho; transformar relatos vagos em comportamento esperado versus atual, contexto, passos de reprodução, evidências e critérios verificáveis; distinguir prioridade de severidade.
3. **Debugger e análise de causa raiz** — reproduzir a falha antes da mudança, reduzir o cenário, interpretar erros, stack traces e logs, criar hipóteses, observar o fluxo com breakpoints, stepping, call stack, variáveis, watches e avaliação de expressões, corrigir a causa e proteger o comportamento com teste de regressão.

O raciocínio esperado para uma correção será:

```text
entender o relato
  → definir esperado x atual
  → reproduzir e coletar evidências
  → reduzir o cenário
  → formular e testar hipóteses
  → localizar a causa raiz
  → escrever um teste de regressão
  → aplicar a menor correção coerente
  → executar testes e validar critérios de aceite
  → registrar a evidência do resultado
```

O checkpoint da fase exigirá tanto a entrega do componente quanto a demonstração desse processo em um bug preparado para o exercício. A avaliação considera o uso consciente das ferramentas do IntelliJ, a qualidade das evidências e a capacidade de explicar por que a mudança corrige a causa sem apenas esconder o sintoma.

O conteúdo detalhado, a ordem exata, os objetivos observáveis e os pré-requisitos estão em `curriculum/java.json`.
