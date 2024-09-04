package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;

import java.io.Serializable;

@AllArgsConstructor
public class PDFResponseDTO implements Serializable {
    @JsonProperty("customer_id")
    String customerId;
    @JsonProperty("client_id")
    String clientID;
    @JsonProperty("file_path")
    String CPlink;
}
