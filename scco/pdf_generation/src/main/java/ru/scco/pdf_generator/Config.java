package ru.scco.pdf_generator;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Configuration
public class Config {
    @Value("${rabbit.pdf_generation_exchange}")
    public String pdfGenerationExchange;

    @Value("${rabbit.db_functional_routing_key}")
    public String dbFunctionalRoutingKey;


    @Bean
    TopicExchange pdfExchange(
            @Value("${rabbit.pdf_generation_exchange}") String name) {
        return new TopicExchange(name, true, false);
    }

    @Bean
    Queue inputQueue(@Value("${rabbit.pdf_generation_queue}") String name) {
        return new Queue(name, true);
    }

    @Bean
    Binding pdfBinding(Queue inputQueue, TopicExchange pdfExchange,
                       @Value("${rabbit.pdf_generation_routing_key}")
                       String key) {
        return BindingBuilder.bind(inputQueue).to(pdfExchange).with(key);
    }

    @Bean
    Queue crudResponseQueue(
            @Value("${rabbit.db_response_queue}") String name) {
        return new Queue(name, true);
    }


    @Bean
    Binding crudResponseBinding(Queue crudResponseQueue,
                                TopicExchange pdfExchange,
                                @Value("${rabbit.db_response_routing_key}")
                                String key) {
        return BindingBuilder.bind(crudResponseQueue).to(pdfExchange)
                             .with(key);
    }


    @Bean
    TopicExchange outerExchange(
            @Value("${rabbit.outer_exchange}") String name) {
        return new TopicExchange(name, true, false);
    }

    @Bean
    Queue outerQueue(@Value("${rabbit.outer_queue}") String name) {
        return new Queue(name, true);
    }

    @Bean
    Binding outerBinding(Queue outerQueue, TopicExchange outerExchange,
                         @Value("${rabbit.outer_routing_key}")
                         String key) {
        return BindingBuilder.bind(outerQueue).to(outerExchange).with(key);
    }


    @Bean
    TopicExchange dbExchange(
            @Value("${rabbit.db_functional_exchange}") String name) {
        return new TopicExchange(name, true, false);
    }

    @Bean
    Queue dbQueue(@Value("${rabbit.db_functional_queue}") String name) {
        return new Queue(name, true);
    }

    @Bean
    Binding dbBinding(Queue dbQueue, TopicExchange dbExchange,
                      @Value("${rabbit.db_functional_routing_key}")
                      String key) {
        return BindingBuilder.bind(dbQueue).to(dbExchange).with(key);
    }


    @Bean
    public MessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(messageConverter());
        return rabbitTemplate;
    }

    @Bean
    PDFGenerator pdfGenerator(
            @Value("${pdf_generator.template}") String templatePath,
            @Value("${pdf_generator.font}") String fontPath,
            @Value("${pdf_generator.dest}") String destinationPath,
            @Value("${pdf_generator.fontsize}") int fontSize
    ) {
        return new PDFGenerator(templatePath, fontPath, destinationPath,
                                fontSize);
    }

    @Bean
    ErrorsResponseMessages errorsMessages(
            @Value("${errors.file_error}") String fileError,
            @Value("${errors.db_error}") String dbError
    ) {
        return new ErrorsResponseMessages(fileError, dbError);
    }

    @Bean
    ExecutorService generatorPool() {
        return Executors.newFixedThreadPool(4);
    }

//    @Bean
//    Sender sender(RabbitTemplate template, Binding dbBinding,
//                  Binding outerBinding) {
//        return new Sender(template,
//                          dbBinding.getExchange(),
//                          dbBinding.getRoutingKey(),
//                          outerBinding.getExchange(),
//                          outerBinding.getRoutingKey()
//        );
//    }
}
