# Arquitetura da V1

## Responsabilidades

1. **Curriculum** — `curriculum/java.json` define módulos, aulas, objetivos, pré-requisitos e checkpoints.
2. **Learning State** — `.learning/` e `scripts/learning.py` persistem e validam a máquina de estados.
3. **Evaluation** — testes JUnit expressam o comportamento esperado; o Codex analisa a aderência ao conceito e gerencia feedback temporário.

Essas responsabilidades não compartilham critérios ocultos. O controlador não decide se um algoritmo está pedagogicamente bom; o teste não decide qual aula vem depois; a skill não altera o estado fora das transições válidas.

## Máquina de estados

O controlador persiste estados estáveis e registra também as transições intermediárias no histórico:

```text
READY
  └─ teach ─→ TEACHING
                 └─ assign ─→ WAITING_FOR_STUDENT
                                    └─ review-start ─→ REVIEWING
                                           ├─ needs-correction ─→ WAITING_FOR_STUDENT
                                           └─ passed ─→ READY (via PASSED e COMPLETED)
```

Uma interrupção em qualquer estado é recuperável por `learning.py continue`.

## Limite de escrita

Todos os caminhos de exercício são resolvidos contra a raiz do projeto. O controlador rejeita caminhos absolutos, travessia (`..`) e arquivos fora de `src/main/java` ou `src/test/java`.

## Feedback

O marcador canônico é:

```java
// DEV_LEARNING_FEEDBACK[LOGIC]: Que condição deveria impedir este caso?
```

Os marcadores são temporários. A aprovação falha enquanto qualquer marcador existir no Java do aluno.
