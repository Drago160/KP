import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import ru.scco.pdf_generator.InvalidCPException;
import ru.scco.pdf_generator.processors.DeleteName;

public class DeleteNameTest {
    private final DeleteName deleteName = new DeleteName();
    @Test
    public void deleteWithoutAndAllLowercase() throws InvalidCPException {
        Assertions.assertEquals("Здравствуйте, я менеджер компании Орифлейм",
                                deleteName.process("Здравствуйте, меня зовут "
                                                   + "Елена, я менеджер компании Орифлейм"));
    }
    @Test
    public void deleteWithoutAndLowercaseToUppercase() throws InvalidCPException {
        Assertions.assertEquals("Здравствуйте! Я менеджер компании Орифлейм",
                                deleteName.process("Здравствуйте! Меня зовут "
                                                   + "Елена, я менеджер компании Орифлейм"));
    }

    @Test
    public void deleteWithAndAllLowercase() throws InvalidCPException {
        Assertions.assertEquals("Здравствуйте, я менеджер компании Орифлейм",
                                deleteName.process("Здравствуйте, меня зовут "
                                                   + "Елена, и я менеджер "
                                                   + "компании Орифлейм"));

    }

    @Test
    public void deleteWithAndLowercaseToUppercase() throws InvalidCPException {
        Assertions.assertEquals("Здравствуйте! Я менеджер компании Орифлейм",
                                deleteName.process("Здравствуйте! Мое имя "
                                                   + "Елена, и я менеджер "
                                                   + "компании Орифлейм"));

    }







}
