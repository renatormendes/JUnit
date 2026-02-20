import static org.junit.Assert.assertEquals;

public class Main {

	public static void main(String[] args) {

		Calculadora calc = new Calculadora();
		
		assertEquals(30, calc.somar(10, 20));
		assertEquals(10, calc.subtrair(10, 20));
		assertEquals(15, calc.multiplicar(5, 3));
		assertEquals(2, calc.dividir(10, 20));

	}
}