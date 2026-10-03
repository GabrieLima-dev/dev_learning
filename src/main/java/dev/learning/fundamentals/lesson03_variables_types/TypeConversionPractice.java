package dev.learning.fundamentals.lesson03_variables_types;

public final class TypeConversionPractice {

    // TODO: ajuste ESTE campo existente para representar o limite diário de 120 visitantes.
    // Ele deve continuar como int, pois 120 é uma quantidade inteira; não crie outra variável nem use Integer aqui.
    // public permite que outras classes consultem o limite, static faz o limite pertencer à classe e final impede reatribuição.
    // Use o valor 120 na inicialização e mantenha o nome em maiúsculas, padrão de constantes.
    public static final int DAILY_VISITOR_LIMIT = 120;

    private TypeConversionPractice() {
    }

    public static int wholeYears(double age) {
        // TODO: use o parâmetro age, que chega como double, para devolver uma idade inteira.
        // Você deve alterar apenas o valor retornado: 21.9 deve resultar em 21, sem arredondar para 22.
        // Como o retorno é int e não guarda casas decimais, faça uma conversão explícita antes de retornar.
        // Não crie outra idade nem modifique o parâmetro recebido.
        int age1 = (int) age;
        return age1;
    }

    public static double asDecimalQuantity(int quantity) {
        // TODO: transforme quantity, que chega como int, em um valor double com a mesma quantidade.
        // Por exemplo, 8 deve retornar 8.0: o número não muda, apenas passa a ter formato decimal.
        // Crie uma variável local var para guardar o valor decimal e retorne essa variável.
        // Não some, subtraia ou altere quantity; a tarefa é somente converter o tipo.
        var quantidade = (double) quantity;
        return quantidade;
    }

    public static Integer boxedBadgeNumber(int badgeNumber) {
        // TODO: receba o int badgeNumber e devolva um objeto Integer com o mesmo número dentro.
        // Por exemplo, ao receber 15, o resultado deve ser um Integer que representa 15, não texto e não null.
        // Use a classe wrapper Integer para criar ou obter esse objeto e retorne-o.
        // Não altere o valor recebido nem crie uma regra nova para o número do crachá.

        Integer number = badgeNumber;
        return number;
    }

    public static int unboxedBadgeNumber(Integer badgeNumber) {
        // TODO: receba o objeto Integer badgeNumber e devolva o número int que está dentro dele.
        // Por exemplo, um Integer com valor 15 deve retornar o int 15; o resultado não pode continuar sendo um objeto.
        // Extraia o valor primitivo do wrapper e retorne-o sem fazer cálculos ou transformá-lo em texto.
        // Nesta prática, badgeNumber sempre terá valor; você não precisa tratar null.
        int number = badgeNumber;
        return number;
    }

    public static int visitorNumberFromText(String text) {
        // TODO: receba o texto numérico text e devolva o número int que ele representa.
        // Por exemplo, "42" deve resultar em 42: o retorno é um número, não a String recebida.
        // Use a conversão oferecida pela wrapper Integer para interpretar o texto antes de retornar.
        // Nesta prática, text sempre contém um número inteiro válido; não crie tratamento de erro ainda.
        int number = Integer.parseInt(text);
        return number;
    }
}
