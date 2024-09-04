package ru.scco.pdf_generator.processors;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SentenceProcessingChain implements ProcessNode {
    List<SentenceProcessNode> processNodeList;

    private List<String> splitSentence(String text) {
        Pattern pattern = Pattern.compile("[.!?;]");
        Matcher matcher = pattern.matcher(text);
        List<String> sentences = new ArrayList<>();

        int start = 0;
        while (matcher.find()) {
            if (start < matcher.start()) {
                sentences.add(text.substring(start, matcher.start()));
            }
            sentences.add(text.substring(matcher.start(), matcher.end()));
            start = matcher.end();
        }

        if (start < text.length()) {
            sentences.add(text.substring(start));
        }

        return sentences;
    }

    @Override
    public String process(String cp) {
        List<String> sentences = splitSentence(cp);
        for (SentenceProcessNode node : processNodeList) {
            node.process(sentences);
        }
        return String.join("", sentences);
    }
}
