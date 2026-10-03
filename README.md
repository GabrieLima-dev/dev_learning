# DEV_LEARNING

Uma trilha prática para aprender Java de forma progressiva: você lê o conceito, resolve exercícios com dificuldade crescente, roda os testes e recebe uma revisão antes de seguir para a próxima aula.

## O que você vai aprender

| Fase | Ao final, você será capaz de |
|---|---|
| 1. Fundamentos | Usar IntelliJ IDEA, testes, Git e GitHub; trabalhar com Java básico, tipos, operadores, entrada e saída, decisões, repetições, arrays e textos. |
| 2. Estrutura do código | Organizar comportamentos em métodos, classes, packages, parâmetros, retornos e membros `static`. |
| 3. Orientação a Objetos | Modelar dados e comportamentos com encapsulamento, herança, polimorfismo, composição e interfaces. |
| 4. APIs essenciais | Manipular coleções, generics, enums, records, exceções, `Optional`, números, datas e arquivos. |
| 5. Java funcional e moderno | Escrever transformações com lambdas, Streams, pattern matching, text blocks e imutabilidade. |
| 6. Concorrência | Executar tarefas concorrentes com threads, executors, futures e estruturas seguras. |
| 7. SQL e acesso a dados | Criar acesso relacional com JDBC, CRUD, joins, transações, paginação e migrations. |
| 8. Engenharia de software | Trabalhar com Maven, Git/GitHub, testes, debugging, refatoração, SOLID e logs. |
| 9. Backend com Quarkus | Construir APIs REST com Jakarta EE, DTOs, validação, serviços e injeção de dependência. |
| 10. Persistência com ORM | Persistir o domínio com JPA, Hibernate, relacionamentos, queries e transações. |
| 11. Microsserviços | Integrar serviços com HTTP, resiliência, mensageria, Kafka, Redis e processamento assíncrono. |
| 12. Segurança e observabilidade | Proteger APIs e acompanhar sua operação com OAuth, JWT, OpenAPI, health checks, logs, métricas e traces. |
| 13. Testes e entrega | Validar, empacotar e entregar aplicações com testes de integração, Docker, pipelines e infraestrutura. |
| 14. Integração web e QA | Entender contratos com frontend, Angular, testes de interface e automação de QA. |
| 15. Projeto final | Construir e publicar um microsserviço completo, testado e reproduzível. |

## Antes de começar

Instale estas ferramentas:

- Git;
- Java 25;
- IntelliJ IDEA;
- Python 3.10 ou superior;
- AI Chat com Codex habilitado no IntelliJ IDEA.

O Maven já vem preparado no projeto pelo Maven Wrapper, então não precisa ser instalado separadamente.

## Criar sua cópia do projeto

### Opção recomendada: usar o template

Use esta opção se você quer registrar sua evolução e criar commits no seu próprio repositório.

1. No GitHub, clique em **Use this template**.
2. Escolha **Create a new repository**.
3. Selecione sua conta, dê um nome ao repositório e crie sua cópia.
4. Copie a URL HTTPS ou SSH do repositório que acabou de criar.

Depois, no terminal, execute:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### Opção para estudar localmente: clonar este repositório

Se você quer apenas abrir e estudar o projeto no computador, execute:

```bash
git clone https://github.com/GabrieLima-dev/dev_learning.git
cd dev_learning
```

Esse clone aponta para o repositório original e normalmente não permite enviar alterações. Para guardar sua evolução no GitHub, prefira criar uma cópia pelo template.

## Conferir se o projeto funciona

Sempre execute os comandos a partir da pasta do projeto.

No macOS ou Linux:

```bash
git --version
java --version
python3 --version
./mvnw test
```

No Windows (PowerShell):

```powershell
git --version
java --version
py -3 --version
mvnw.cmd test
```

Se o macOS ou Linux informar que `mvnw` não tem permissão de execução, rode uma vez:

```bash
chmod +x mvnw
```

Depois execute `./mvnw test` novamente. Um resultado com `BUILD SUCCESS` significa que o projeto está pronto.

## Abrir no IntelliJ e iniciar a trilha pelo AI Chat

1. Abra a pasta clonada no IntelliJ IDEA.
2. Abra o painel **AI Chat**.
3. Selecione **Codex** como agente do chat.
4. Escreva:

```text
vamos começar
```

Se você já estudou antes, escreva no mesmo chat:

```text
vamos continuar
```

Não é preciso lembrar em qual aula parou: a trilha retoma o ponto salvo automaticamente. No JetBrains, o fluxo oficial é abrir o AI Chat e selecionar Codex. [Veja a documentação oficial](https://learn.chatgpt.com/docs/codex/ide).

## Como funciona cada aula

Cada aula segue este ciclo:

1. Você recebe um arquivo `CONCEITO_...md` com explicações e exemplos em Java.
2. Você abre o arquivo de prática indicado no conceito e lê os TODOs.
3. Resolve os exercícios em níveis: começa pelo fundamento, aplica o conceito em um caso mais completo e termina com um desafio que reutiliza conhecimentos anteriores quando fizer sentido.
4. Executa os testes.
5. Quando terminar, escreve `terminei` no AI Chat.
6. O Codex executa a suíte, revisa o uso do conceito e indica uma correção se for necessária.
7. Após a aprovação, você revisa as mudanças e cria um commit pequeno e coerente.

Os testes não são um obstáculo escondido: seus nomes e mensagens mostram o comportamento esperado. Quando algo falhar, leia primeiro a mensagem do teste e depois volte ao TODO correspondente.

## Comandos que você usará durante os estudos

Rodar todos os testes no macOS ou Linux:

```bash
./mvnw test
```

Rodar todos os testes no Windows:

```powershell
mvnw.cmd test
```

Depois da aula inicial de Git, você também praticará estes comandos antes de criar seus commits:

```bash
git status
git diff
git diff --staged
git log --oneline
```

Evite `git add .` como atalho. Revise os arquivos e prepare somente os que pertencem à atividade que você concluiu.

## Frases úteis para usar no AI Chat

```text
vamos começar
vamos continuar
terminei
resumo da última aula
quero revisar collections
```

## Projeto final

No final da trilha, você reunirá os conhecimentos em um microsserviço. Ele deverá ter testes verdes, instruções de execução, histórico Git organizado, configuração segura e um repositório GitHub atualizado.

## Licença

Este projeto utiliza a [DEV_LEARNING Mixed License 1.0](LICENSE.md). Consulte o arquivo de licença para conhecer os termos de uso do material e do núcleo da trilha.
