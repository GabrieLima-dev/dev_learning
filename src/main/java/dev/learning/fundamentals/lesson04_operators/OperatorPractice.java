package dev.learning.fundamentals.lesson04_operators;

public final class OperatorPractice {

    private OperatorPractice() {
    }

    // Exercício 1 — Total aritmético
    public static double deliveryTotal(double itemPrice, int quantity, double discount) {
        // TODO: use itemPrice, quantity e discount para devolver o valor final de uma entrega.
        // Primeiro considere o preço de todos os itens e depois aplique o desconto recebido.
        // Exemplo: preço 12.5, quantidade 3 e desconto 5.0 devem resultar em 32.5.
        // Não altere os parâmetros nem arredonde o resultado; use uma expressão aritmética no retorno.
        return (itemPrice * quantity) - discount;
    }

    // Exercício 2 — Regra relacional e lógica
    public static boolean canReceiveDelivery(int age, boolean hasDocument) {
        // TODO: devolva true somente quando age for pelo menos 18 e hasDocument também for true.
        // Exemplo: 20 e true resultam em true; 17 e true, ou 20 e false, resultam em false.
        // Combine a comparação da idade com a informação booleana recebida em uma única expressão.
        // Não crie if/else: esta prática exercita operadores relacionais e lógicos.
        return age >= 18 && hasDocument;
    }

    // Exercício 3 — Mensagem ternária
    public static String deliveryStatus(boolean canReceive) {
        // TODO: devolva uma mensagem a partir de canReceive usando uma expressão ternária.
        // Quando for true, o resultado é "Entrega liberada"; quando for false, é "Entrega bloqueada".
        // Use somente esse parâmetro e retorne uma das duas Strings, sem criar if/else.
        return canReceive ? "Entrega liberada" : "Entrega bloqueada";
    }

    // Exercício 4 — Resto e comparação
    public static boolean isEvenOrderNumber(int orderNumber) {
        // TODO: devolva true quando orderNumber for par e false quando for ímpar.
        // Exemplo: 24 resulta em true e 25 resulta em false; use o próprio número recebido.
        // Produza uma expressão que descubra o resto da divisão por dois e compare esse resultado.
        int divisao = orderNumber % 2;
        return divisao == 0;

    }

    // Exercício 5 — Desafio cumulativo: wrappers, var e aritmética
    public static Integer netDeliveryScore(Integer deliveredOrders, int cancelledOrders) {
        // TODO: use deliveredOrders e cancelledOrders para devolver a pontuação líquida como um objeto Integer.
        // Primeiro obtenha o valor numérico do wrapper, considere os pedidos cancelados e guarde o resultado em uma variável local var.
        // Exemplo: um Integer com 12 entregas e 3 cancelamentos devem resultar em um Integer com valor 9.
        // Este desafio reutiliza wrappers e var da aula anterior com a expressão aritmética desta aula; deliveredOrders nunca será null.

        var i = deliveredOrders - cancelledOrders;
        return i;



    }
}
