package ru.scco.pdf_generator.dto;

import java.io.Serializable;

public record PDFStatusResponseDTO(long userId, boolean status,
                                   String comment) implements Serializable {
}
