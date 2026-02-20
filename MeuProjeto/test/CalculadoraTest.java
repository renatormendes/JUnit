import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class CalculadoraTest {

	@Test
	void testeSoma() {

		assertEquals(2, 1 + 1);

	}

	@Test
	void testeSubtrair() {

		assertEquals(0, 1 - 1);

	}

	@Test
	void testeMultiplicar() {

		assertEquals(10, 2 * 5);

	}

	@Test
	void testeDividir() {

		assertEquals(5, 10 / 2);
		
	}
}