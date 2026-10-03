# Variáveis, tipos, conversões e wrappers

Uma variável é um nome que usamos para guardar um valor enquanto o programa executa. Ao declarar uma variável em Java, escolhemos o seu tipo: ele informa qual espécie de dado será armazenada e quais operações fazem sentido com ela. Esse cuidado evita ambiguidades, torna o código mais claro e permite que o compilador encontre usos incompatíveis antes de executar o programa.

Os tipos primitivos representam valores simples. `int` guarda números inteiros, como uma quantidade de visitantes; `double` guarda números com parte decimal, como uma medida de temperatura; `boolean` representa `true` ou `false`; e `char` guarda um único caractere, como uma letra de setor. Cada variável local precisa receber um valor antes de ser usada. Neste exemplo, cada linha declara uma variável: o primeiro termo é o tipo, o segundo é o nome que escolhemos e, depois de `=`, vem o valor inicial.

```java
int booksOnShelf = 24;
double distanceInKm = 12.5;
boolean libraryIsOpen = true;
char roomLetter = 'B';
String readerName = "Lia";
```

`booksOnShelf` é uma contagem, então usa `int`; `distanceInKm` aceita frações, então usa `double`; `libraryIsOpen` só pode ser verdadeiro ou falso; `roomLetter` guarda uma letra entre aspas simples; e `readerName` guarda texto entre aspas duplas.

Tipos de referência guardam uma referência para um objeto. `String` é um exemplo comum: `String visitorName = "Lia";` representa um texto. A diferença importante neste começo é que um primitivo contém diretamente o seu valor, enquanto uma referência aponta para um objeto. Evite assumir que todo valor numérico cabe em qualquer tipo: escolha o tipo pelo significado do dado, não apenas pelo exemplo atual.

Quando um valor não deve mudar, use `final`. Uma constante é uma variável `final` associada a um valor fixo e normalmente recebe um nome em letras maiúsculas, como `MAXIMUM_CAPACITY`. O nome deixa explícito que aquele dado não deve ser reatribuído. Uma constante não é só uma convenção visual: o compilador impede uma nova atribuição depois que ela foi inicializada.

```java
public static final int MAXIMUM_BORROWED_BOOKS = 5;
```

Nesse exemplo, `int` mostra que o limite é inteiro, `public` permite que outras classes o consultem, `static` faz o limite pertencer à classe inteira e `final` impede que o valor `5` seja trocado depois. O nome em maiúsculas indica que é um valor fixo do domínio.

Java também oferece `var` para variáveis locais. Com `var`, o compilador descobre o tipo a partir do valor da inicialização. Isso não cria um tipo “sem definição”: o tipo continua existindo e é decidido na compilação.

```java
var sectionName = "Literatura"; // o compilador infere String
```

Use `var` quando o tipo for evidente pelo valor à direita; não o use para campos da classe, parâmetros, valores sem inicialização ou quando esconder o tipo deixaria a leitura difícil.

Uma conversão muda a forma como um valor é tratado por outro tipo. Converter um `int` para `double` preserva o valor; já converter um `double` para `int` pode descartar a parte decimal. Por essa possível perda de informação, a conversão para um tipo mais restrito precisa ser explícita, usando um cast.

```java
int borrowedBooks = 8;
double decimalBooks = borrowedBooks; // 8 se torna 8.0 automaticamente

double lateFee = 19.7;
int wholeFee = (int) lateFee; // 19.7 se torna 19; não arredonda para 20
```

No primeiro caso, `double` consegue representar o inteiro sem perda. No segundo, `(int)` é o cast: ele avisa que a parte decimal será descartada. Antes de converter, pense no que deve acontecer com a informação que não cabe no tipo de destino; não faça casts apenas para silenciar o compilador.

Para cada primitivo, Java tem uma classe wrapper equivalente: `int` corresponde a `Integer`, `double` a `Double`, `boolean` a `Boolean` e assim por diante. Wrappers permitem tratar valores primitivos como objetos quando uma API precisa de objetos.

```java
int shelfNumber = 37;
Integer shelfNumberObject = Integer.valueOf(shelfNumber); // boxing
int shelfNumberAgain = shelfNumberObject.intValue(); // unboxing
int aisle = Integer.parseInt("12"); // texto numérico vira int
```

A passagem de `int` para `Integer` é chamada de boxing; o caminho inverso é unboxing. `Integer.parseInt` interpreta os caracteres de um texto numérico e devolve um `int`. Ao lidar com uma wrapper, lembre-se de que ela pode ser `null`; nesta prática, os testes sempre fornecem um valor válido.

Erros comuns nesta aula incluem escolher `double` quando o dado é uma contagem inteira, usar `var` sem uma inicialização clara, tentar alterar uma constante e esperar que uma conversão para `int` arredonde automaticamente. Ela não arredonda: a parte decimal é removida. Também não misture a representação textual de um número com o próprio valor numérico; um `String` com `"42"` ainda é texto até ser convertido.

Agora abra [TypeConversionPractice.java](./TypeConversionPractice.java) e realize os TODOs.

Quando finalizar, execute `./mvnw test` no macOS ou Linux, ou `mvnw.cmd test` no Windows. Você pode abrir [TypeConversionPracticeTest.java](../../../../../../test/java/dev/learning/fundamentals/lesson03_variables_types/TypeConversionPracticeTest.java) para consultar os comportamentos verificados.
