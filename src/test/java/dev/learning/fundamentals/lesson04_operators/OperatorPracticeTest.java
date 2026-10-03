package dev.learning.fundamentals.lesson04_operators;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class OperatorPracticeTest {

    @Test
    void valorDaEntregaConsideraQuantidadeEDesconto() {
        assertEquals(
                32.5,
                OperatorPractice.deliveryTotal(12.5, 3, 5.0),
                "12.5 por item, 3 itens e desconto de 5.0 devem resultar em 32.5."
        );
    }

    @Test
    void entregaExigeMaioridadeEDocumento() {
        assertTrue(
                OperatorPractice.canReceiveDelivery(20, true),
                "Uma pessoa de 20 anos com documento pode receber a entrega."
        );
        assertFalse(
                OperatorPractice.canReceiveDelivery(17, true),
                "Uma pessoa menor de 18 anos não pode receber a entrega."
        );
        assertFalse(
                OperatorPractice.canReceiveDelivery(20, false),
                "A ausência de documento bloqueia a entrega."
        );
    }

    @Test
    void statusUsaAsDuasMensagensDefinidas() {
        assertEquals(
                "Entrega liberada",
                OperatorPractice.deliveryStatus(true),
                "O status true deve gerar a mensagem de entrega liberada."
        );
        assertEquals(
                "Entrega bloqueada",
                OperatorPractice.deliveryStatus(false),
                "O status false deve gerar a mensagem de entrega bloqueada."
        );
    }

    @Test
    void numeroDePedidoParTemRestoZeroNaDivisaoPorDois() {
        assertTrue(OperatorPractice.isEvenOrderNumber(24), "24 é um número par.");
        assertFalse(OperatorPractice.isEvenOrderNumber(25), "25 é um número ímpar.");
    }

    @Test
    void pontuacaoLiquidaReutilizaWrapperVarEAritmetica() {
        assertEquals(
                Integer.valueOf(9),
                OperatorPractice.netDeliveryScore(Integer.valueOf(12), 3),
                "12 entregas e 3 cancelamentos devem produzir um Integer com valor 9."
        );
    }
}
