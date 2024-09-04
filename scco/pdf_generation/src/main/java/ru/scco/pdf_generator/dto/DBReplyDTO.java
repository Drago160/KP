package ru.scco.pdf_generator.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

public class DBReplyDTO implements Serializable {
    @JsonProperty("exchange")
    String exchange;
    @JsonProperty("routing_key")
    String routingKey;

    public DBReplyDTO(String exchange, String routingKey) {
        this.exchange = exchange;
        this.routingKey = routingKey;
    }

}
