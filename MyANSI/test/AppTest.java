import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import app.App;

class AppTest {

    @Test 
    void testSomar() {

        assertEquals(2, new App().somar(1,1));

    }

    @Test 
    void testSubtrair() {

        assertEquals(2, new App().subtrair(5,3));

    }
    
}