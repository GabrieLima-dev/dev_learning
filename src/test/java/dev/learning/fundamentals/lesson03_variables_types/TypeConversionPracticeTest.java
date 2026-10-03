package dev.learning.fundamentals.lesson03_variables_types;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import org.junit.jupiter.api.Test;

class TypeConversionPracticeTest {

    @Test
    void limiteDiarioDeveTerValorFixoDe120() throws NoSuchFieldException {
        Field limit = TypeConversionPractice.class.getField("DAILY_VISITOR_LIMIT");

        assertTrue(
                Modifier.isFinal(limit.getModifiers()),
                "DAILY_VISITOR_LIMIT deve ser uma constante: use final para impedir nova atribuição."
        );
        assertEquals(
                120,
                TypeConversionPractice.DAILY_VISITOR_LIMIT,
                "DAILY_VISITOR_LIMIT deve representar o limite diário de 120 visitantes."
        );
    }

    @Test
    void idadeComDecimalDeveVirarApenasAnosInteiros() {
        assertEquals(
                21,
                TypeConversionPractice.wholeYears(21.9),
                "wholeYears(21.9) deve descartar a parte decimal e devolver 21."
        );
    }

    @Test
    void quantidadeInteiraDeveSerRepresentadaComoDecimal() {
        assertEquals(
                8.0,
                TypeConversionPractice.asDecimalQuantity(8),
                "asDecimalQuantity(8) deve devolver o mesmo valor na forma decimal: 8.0."
        );
    }

    @Test
    void numeroPrimitivoDeveVirarUmObjetoInteger() {
        assertEquals(
                Integer.valueOf(15),
                TypeConversionPractice.boxedBadgeNumber(15),
                "boxedBadgeNumber(15) deve devolver um Integer com valor 15."
        );
    }

    @Test
    void objetoIntegerDeveVoltarParaValorPrimitivo() {
        assertEquals(
                15,
                TypeConversionPractice.unboxedBadgeNumber(Integer.valueOf(15)),
                "unboxedBadgeNumber deve extrair o int 15 do Integer recebido."
        );
    }

    @Test
    void textoNumericoDeveSerConvertidoParaInteiro() {
        assertEquals(
                42,
                TypeConversionPractice.visitorNumberFromText("42"),
                "visitorNumberFromText(\"42\") deve converter o texto em int 42."
        );
    }
}
