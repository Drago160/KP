package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.io.Serializable;

@AllArgsConstructor
@Data
public class DBInsertRequestData implements Serializable {
    @JsonProperty("message_group_id")
    long messageGroupID;
    @JsonProperty("file_path")
    String filePath;
}
