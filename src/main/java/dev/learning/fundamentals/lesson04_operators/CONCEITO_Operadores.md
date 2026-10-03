# Operadores

Operadores são símbolos que combinam valores e produzem um novo resultado. Eles aparecem dentro de expressões: uma expressão pode calcular um número, comparar valores ou produzir `true` e `false`. Nesta aula, você usará operadores aritméticos, relacionais, lógicos e a expressão ternária.

Operadores aritméticos trabalham com números. `+` soma, `-` subtrai, `*` multiplica, `/` divide e `%` devolve o resto de uma divisão. Veja um exemplo com empréstimos de uma biblioteca:

```java
int booksBorrowed = 3;
int extraBooks = 2;
int totalBooks = booksBorrowed + extraBooks;
int booksPerShelf = totalBooks / 5;
int remainingBooks = totalBooks % 5;
```

`totalBooks` recebe `5`. A divisão inteira em `booksPerShelf` resulta em `1`, porque ambos os valores são `int`. `remainingBooks` recebe `0`, pois cinco não deixa resto quando é dividido por cinco. Para obter resultado com casas decimais, pelo menos um dos valores da divisão precisa ser `double`.

Operadores relacionais comparam dois valores e sempre produzem um `boolean`. Eles são `>`, `>=`, `<`, `<=`, `==` e `!=`.

```java
int availableBooks = 7;
boolean hasEnoughBooks = availableBooks >= 5;
boolean libraryIsEmpty = availableBooks == 0;
```

No primeiro resultado, `hasEnoughBooks` é `true`, porque sete é maior ou igual a cinco. No segundo, `libraryIsEmpty` é `false`. Atenção: `=` atribui um valor a uma variável, enquanto `==` compara dois valores.

Operadores lógicos combinam valores booleanos. `&&` resulta em `true` somente se os dois lados forem verdadeiros; `||` resulta em `true` quando pelo menos um lado é verdadeiro; `!` inverte um booleano.

```java
boolean hasLibraryCard = true;
boolean hasNoOverdueBooks = false;
boolean canBorrow = hasLibraryCard && hasNoOverdueBooks;
boolean needsHelpDesk = !hasLibraryCard || !hasNoOverdueBooks;
```

`canBorrow` é `false`, pois uma condição é falsa. `needsHelpDesk` é `true`, pois basta uma das condições ao redor de `||` ser verdadeira. Use parênteses quando uma expressão tiver várias comparações e operadores lógicos: eles tornam a intenção mais fácil de ler.

A expressão ternária escolhe um de dois valores usando uma condição. Sua forma é `condição ? valorSeVerdadeiro : valorSeFalso`.

```java
boolean canBorrow = true;
String message = canBorrow ? "Empréstimo liberado" : "Empréstimo bloqueado";
```

Como `canBorrow` é `true`, `message` recebe `"Empréstimo liberado"`. A ternária é útil quando a decisão apenas produz um valor; decisões com vários passos serão estudadas depois, com condicionais.

Erros frequentes são confundir `=` com `==`, esquecer que a divisão entre inteiros elimina a parte decimal, usar `&&` quando bastaria uma condição com `||` e inverter as duas mensagens da ternária. Leia a expressão da esquerda para a direita e confirme o tipo de resultado esperado: número, texto ou booleano.

## Progressão da prática

Você fará cinco exercícios, do mais direto ao mais completo. No **Exercício 1**, aplique uma expressão aritmética a `double` e `int`. No **Exercício 2**, produza um `boolean` combinando uma comparação de idade e uma informação booleana. No **Exercício 3**, use a ternária para escolher entre duas mensagens. No **Exercício 4**, use o resto de uma divisão para identificar números pares. No **Exercício 5**, reúna a aritmética desta aula com `Integer` e `var`, que você aprendeu na aula anterior. Resolva na ordem: cada nível prepara o próximo.

Agora abra [OperatorPractice.java](./OperatorPractice.java) e realize os TODOs.

Quando finalizar, execute `./mvnw test` no macOS ou Linux, ou `mvnw.cmd test` no Windows. Você pode abrir [OperatorPracticeTest.java](../../../../../../test/java/dev/learning/fundamentals/lesson04_operators/OperatorPracticeTest.java) para consultar os comportamentos verificados.
