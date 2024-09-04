import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import ru.scco.pdf_generator.PDFGenerator;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class PDFGeneratorTest {
    @Test
    void generationTest() throws IOException {
        Path tempDir = Files.createTempDirectory("pdfgeneration");
        new PDFGenerator("/templates/cp1.pdf",
                         "/fonts/LiberationSansRegular.ttf",
                         tempDir.toString() + "/", 18)
                .generate(1, "Здравствуйте, Акакий "
                             + "Акакиевич!\nМы"
                             + " увидели ваше"
                             + " сообщение в канале @overcoat. Хотим предложить "
                             + "вам свои услуги. Наша команда OwlWeb занимается "
                             + "пошивом шинелей 181 год. "
                             + "Если вас заинтересовало предложение — напишите "
                             + "ответ на сообщение или позвоните нашему "
                             + "менеджеру\n",
                          "Корпоративный менеджер,\n"
                          + "Гоголь Григорий Петрович\n"
                          + "+79995771202");
        Assertions.assertTrue(Files.exists(Path.of(tempDir.toString(),
                                                   "1.pdf")));
    }
}
