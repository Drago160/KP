package ru.scco.pdf_generator.processors;

import org.springframework.stereotype.Component;
import ru.scco.pdf_generator.InvalidCPException;

import java.util.ArrayList;
import java.util.List;

@Component
public class ProcessingChain implements ProcessNode {
    private final static String punctuation = "[.!?;\n]";
    private final static String notPunctuation = "[^.!?;\n]";
    private final static String endOfPreviousSentence =
            "(?:^|" + punctuation + ")";
    private final static String endOfSentence = "(?:$|" + punctuation + ")";
    private final static String anythingInsideSentence = notPunctuation + "*";


    List<ProcessNode> processNodeList = new ArrayList<>();

    public ProcessingChain() {
        processNodeList.add(new DeleteName());
        processNodeList.add(new DeleteInPart(
                0.7f, 1,
                endOfPreviousSentence +
                anythingInsideSentence +
                "[у|У]важени" +
                anythingInsideSentence +
                endOfSentence));
        processNodeList.add(new DeleteInPart(0, 1,
                                             endOfPreviousSentence
                                             + anythingInsideSentence + "\\["
                                             + anythingInsideSentence + "\\]"
                                             + anythingInsideSentence
                                             + endOfSentence));

    }

    ProcessingChain append(ProcessNode processNode) {
        processNodeList.add(processNode);
        return this;
    }

    public String process(String cp) throws InvalidCPException {
        for (ProcessNode node : processNodeList) {
            String newCP = node.process(cp);
            if (newCP != null) {
                cp = newCP;
            }
        }
        if (cp.length() < 100) {
            throw new InvalidCPException("too small CP");
        }
        return cp;
    }
}
