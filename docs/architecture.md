# Arquitetura da V1

## Responsabilidades

1. **Curriculum** — `curriculum/java.json` define módulos, aulas, objetivos, pré-requisitos e checkpoints.
2. **Learning State** — `.learning/` e `scripts/learning.py` persistem e validam a máquina de estados, incluindo os caminhos do conceito, source e teste da aula ativa.
3. **Evaluation** — testes JUnit expressam o comportamento esperado; o Codex analisa a aderência ao conceito e gerencia feedback temporário.

Essas responsabilidades não compartilham critérios ocultos. O controlador não decide se um algoritmo está pedagogicamente bom; o teste não decide qual aula vem depois; a skill não altera o estado fora das transições válidas.

## Máquina de estados

O controlador persiste estados estáveis e registra também as transições intermediárias no histórico:

```text
READY
  ├─ skip-diagnostic ───────────────────────────────→ READY (próxima aula)
  └─ teach ─→ TEACHING
                 ├─ skip-diagnostic ────────────────→ READY (próxima aula)
                 └─ assign ─→ WAITING_FOR_STUDENT
                                    ├─ skip-diagnostic ─→ READY (próxima aula)
                                    └─ review-start ─→ REVIEWING
                                           ├─ needs-correction ─→ WAITING_FOR_STUDENT
                                           └─ passed ─→ READY (via PASSED e COMPLETED)
```

Uma interrupção em qualquer estado é recuperável por `learning.py continue`.
`skip-diagnostic` é aceito somente no diagnóstico inicial. Se o exercício já existir, seus arquivos são preservados com o sufixo `.skipped`, fora da compilação das próximas atividades.

Em trilhas novas, `intellij-idea-foundations` é sempre a primeira aula regular após o diagnóstico. Para preservar trabalho criado antes dessa inclusão, uma atividade de Git que já esteja em andamento pode ser concluída; a próxima aula liberada será então a introdução obrigatória ao IntelliJ IDEA.

## Limite de escrita

Todos os caminhos de exercício são resolvidos contra a raiz do projeto. O controlador rejeita caminhos absolutos, travessia (`..`) e arquivos fora de `src/main/java` ou `src/test/java`. Ao registrar a atividade, também exige o arquivo `CONCEITO_NomeDaAula.md` na mesma pasta do source Java e a pasta canônica `lessonNN_nome_da_aula`, igual para source e teste. O nome é um identificador Java válido, é espelhado no último segmento do `package` e contém a posição entre as aulas regulares com no mínimo dois dígitos. O diagnóstico inicial usa `lesson00_diagnostico_inicial`; o currículo pode definir `directoryName`, como em `lesson01_intellij` e `lesson02_git`.

## Feedback

O marcador canônico é:

```java
// DEV_LEARNING_FEEDBACK[LOGIC]: Que condição deveria impedir este caso?
```

Os marcadores são temporários. A aprovação falha enquanto qualquer marcador existir no Java do aluno.
