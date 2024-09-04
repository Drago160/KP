# README\_INTERACTION



## Взаимодействие с другими сервисами



### Чтение КП

Класс Receiver, метод consume. Сервис читает из очереди ${PDF\_GENERATION\_QUEUE} json вида (вместо значения в примере указан необходимый тип).&#x20;

```
{
message_group_id: long,
main_text: String,
contact_info: String
}
```

Этому Json соответствует **PDFRequestDTO**

### Сохранение в БД

Класс Sender, метод sendCPToDB. Сервис пишет в ${DB\_FUNCTIONAL\_SERVICE\_EXCHANGE} c routing ${DB\_FUNCTIONAL\_SERVICE\_ROUTING\_KEY} json вида (если в примере значение фиксировано, оно указано, иначе указан его тип)

```
{
"request_name": "insert_offers",
"request_data": [
                    {
                        "message_group_id": long,
                        "file_path": String
                    }
                 ],
"reply": {
             "exchange": ${PDF_GENERATION_EXCHANGE},
             "routing_key": ${PDF_GENERATION_ROUTING_KEY}_db_response
         }
}
```

Одному элементу "request\_data" соответствует DBInsertRequestDataDTO.java

"reply" соответствует DBReplyDTO.java

Всему json соответствует DBRequestDTO.java



### Чтение ответа БД

Класс Receiver , метод consumeDBResponse

Читает из ${PDF\_GENERATION\_QUEUE}\_db\_response json вида

```
{
"array_data": [
    {    
        "customer_id": String,
        "client_id": String,
        "file_path": String
    }
]
}
```

1 элементу "array\_fata" соответствует DBInsertOneResponseDTO

Всему json соответствует DBInsertAllResponseDTO





### Запись в сторонню очередь

Класс Sender, метод sendCPToOutput.

Пишет в ${GENERATED\_OFFERS\_EXCHANGE} c routing ${GENERATED\_OFFERS\_ROUTING\_KEY} json вида

```
{
"customer_id": String,
"client_id": String,
"file_path": String
}
```

Ему соответсвует PDFResponseDTO



### Замечение:

При взаимодействии с БД отправляется и принимается список. Это сделано из-за особенностей сервиса БД. На самом деле в программа всегда отправляет и получает ровно один элемент



