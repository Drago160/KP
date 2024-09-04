package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.io.Serializable;

@Data
public class DBInsertOneResponseDTO implements Serializable {
    @JsonProperty("customer_id")
    String customerID;
    @JsonProperty("client_id")
    String clientID;
    @JsonProperty("file_path")
    String filePath;


}
