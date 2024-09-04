package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class DBRequestDTO implements
                          Serializable {
    @JsonProperty("request_name")
    final String requestName = "insert_offers";

    @JsonProperty("request_data")
    List<DBInsertRequestData> responseDTOs = new ArrayList<>();

    @JsonProperty("reply")
    DBReplyDTO dbReplyDTO;

    public DBRequestDTO(DBInsertRequestData requestData, DBReplyDTO replyDTO) {
        this.responseDTOs.add(requestData);
        this.dbReplyDTO = replyDTO;
    }
}