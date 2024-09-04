package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

public record PDFGeneratorRequestDTO(
        @JsonProperty("message_group_id") long messageId,
        @JsonProperty("main_text") String mainText,
        @JsonProperty("contact_info") String contactInfo) implements
                                                          Serializable {
}
