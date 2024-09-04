package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;
import ru.scco.pdf_generator.dto.DBInsertRequestData;
import ru.scco.pdf_generator.dto.DBReplyDTO;
import ru.scco.pdf_generator.dto.DBRequestDTO;
import ru.scco.pdf_generator.dto.PDFResponseDTO;

@Component
@RequiredArgsConstructor
@Slf4j
public class Sender {
    private final RabbitTemplate template;
    private final Binding crudResponseBinding;
    private final Binding dbBinding;
    private final Binding outerBinding;
//    private final String dbFunctionalExchange;
//    private final String dbFunctionalRoutingKey;
//
//    private final String outerExchange;
//    private final String outerRoutingKey;

    public void sendCPToDB(long messageID, String fileLink) {
        log.info("sendCPToDB" + messageID + " " + fileLink);
        log.info("sendCPToDB" + " dist exch: " + dbBinding.getExchange() +
                 " " + "dist routing " + dbBinding.getRoutingKey() + " answ "
                 + "exch: " + crudResponseBinding.getExchange() + " answ "
                 + "routing " + crudResponseBinding.getRoutingKey());
        template.convertAndSend(dbBinding.getExchange(),
                                dbBinding.getRoutingKey(),
                                new DBRequestDTO(
                                        new DBInsertRequestData(messageID,
                                                                fileLink
                                        ), new DBReplyDTO(
                                        crudResponseBinding.getExchange(),
                                        crudResponseBinding.getRoutingKey())));
    }

    public void sendCPToOutput(String customerID, String clientID,
                               String fileLink) {
        log.info("sendCPToOutput " + outerBinding.getExchange() + " "
                 + outerBinding.getRoutingKey());
        template.convertAndSend(outerBinding.getExchange(),
                                outerBinding.getRoutingKey(),
                                new PDFResponseDTO(customerID, clientID,
                                                   fileLink));
    }

    public void sendError(long userId,
                          String errorMessage) {
        // Пока никуда
//        template.convertAndSend(dbFunctionalExchange,
//                                dbFunctionalRoutingKey,
//                                new PDFStatusResponseDTO(userId, false,
//                                                         errorMessage));
    }
}
