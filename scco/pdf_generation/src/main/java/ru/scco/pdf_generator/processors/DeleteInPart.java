package ru.scco.pdf_generator.processors;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DeleteInPart implements ProcessNode {
    private final float partStart;
    private final float partEnd;
    private final Pattern pattern;

    public DeleteInPart(float partStart, float partEnd, String regex) {
        this.partStart = partStart;
        this.partEnd = partEnd;
        this.pattern = Pattern.compile(regex);
    }

    @Override
    public String process(String cp) {
        int offset = (int) (partStart * cp.length());
        Matcher deleteMatcher =
                pattern.matcher(cp.substring(offset,
                                             (int) (partEnd * cp.length())));
        int endIndex = 1;
        StringBuilder builder = new StringBuilder();
        while (deleteMatcher.find(endIndex - 1)) {
            if (endIndex == 1) {
                builder.append(cp, 0, deleteMatcher.start() + offset + 1);
            } else {
                builder.append(cp, endIndex + offset,
                               deleteMatcher.start() + offset + 1);
            }
            endIndex = deleteMatcher.end();
        }
        if (endIndex != 1) {
            builder.append(cp, endIndex + offset, cp.length());
            return builder.toString();
        }
        return null;
    }
}
