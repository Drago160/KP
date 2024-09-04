package ru.scco.pdf_generator.processors;

import ru.scco.pdf_generator.InvalidCPException;

public interface ProcessNode {
    String process(String cp) throws InvalidCPException;
}
