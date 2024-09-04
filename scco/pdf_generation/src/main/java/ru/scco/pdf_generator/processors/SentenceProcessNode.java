package ru.scco.pdf_generator.processors;

import java.util.List;

public interface SentenceProcessNode {
    void process(List<String> cp);
}
