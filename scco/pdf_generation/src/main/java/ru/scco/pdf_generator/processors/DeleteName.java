package ru.scco.pdf_generator.processors;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DeleteName implements ProcessNode {

    private final static Pattern namePattern =
            Pattern.compile("([м|М]ое имя|[мМ]еня "
                            + "зовут) "
                            + "([a-яА-ЯёЁ]*)([ .,!?])");

    private static boolean isRussianUppercase(char character) {
        return character >= 'А' && character <= 'Я' || character == 'Ё';
    }

    private static boolean isRussianLowercase(char character) {
        return character >= 'а' && character <= 'я' || character == 'ё';
    }

    @Override
    public String process(String cp) {
        Matcher matcher = namePattern.matcher(cp);
        if (matcher.find()) {
            StringBuilder newCpBuilder = new StringBuilder();
            newCpBuilder.append(cp, 0, matcher.start());
            if (matcher.end() + 1 < cp.length()) {
                int continueTextIndex = matcher.end() + 1;
                if (matcher.end() + 3 < cp.length()
                    && cp.charAt(matcher.end() + 1) == 'и'
                    || cp.charAt(matcher.end() + 1) == 'И') {
                    continueTextIndex = matcher.end() + 3;
                }
                if (isRussianUppercase(matcher.group(1).charAt(0))
                    && isRussianLowercase(cp.charAt(continueTextIndex))) {
                    if (cp.charAt(continueTextIndex) == 'ё') {
                        newCpBuilder.append('Ё');
                    } else {
                        newCpBuilder.append(
                                (char) (cp.charAt(continueTextIndex) - 'а'
                                        + 'А'));
                    }
                } else {
                    newCpBuilder.append(cp.charAt(continueTextIndex));
                }
                newCpBuilder.append(cp, continueTextIndex + 1, cp.length());
            }
            return newCpBuilder.toString();
        }
        return null;
    }
}
