package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.io.Serializable;
import java.util.List;

@Data
public class DBInsertAllResponseDTO implements
                                    Serializable {
    @JsonProperty("array_data")
    List<DBInsertOneResponseDTO> responses;

}
