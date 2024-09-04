import com.rabbitmq.client.Channel;
import lombok.extern.slf4j.Slf4j;
import org.mockito.Mockito;
import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.config.SimpleRabbitListenerContainerFactory;
import org.springframework.amqp.rabbit.connection.Connection;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.test.RabbitListenerTest;
import org.springframework.amqp.rabbit.test.TestRabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import ru.scco.pdf_generator.ErrorsResponseMessages;
import ru.scco.pdf_generator.PDFGenerator;
import ru.scco.pdf_generator.Sender;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import static org.mockito.ArgumentMatchers.anyBoolean;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.willReturn;
import static org.mockito.Mockito.mock;

@Configuration
@RabbitListenerTest(capture = true)
@Slf4j
public class TestConfig {
    @Value("${rabbit.pdf_generation_exchange}")
    private String exchangeName;


    @Bean
    DirectExchange exchange() {
        return new DirectExchange(exchangeName, true, false);
    }

    @Bean
    Queue inputQueue(@Value("${rabbit.pdf_generation_queue}") String name) {
        return new Queue(name, true);
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
    public ConnectionFactory mockConnectionFactory() {
        ConnectionFactory factory = mock(ConnectionFactory.class);
        Connection connection = mock(Connection.class);
        Channel channel = mock(Channel.class);
        willReturn(connection).given(factory).createConnection();
        willReturn(channel).given(connection).createChannel(anyBoolean());
        given(channel.isOpen()).willReturn(true);
        return factory;
    }

    @Bean
    public TestRabbitTemplate testRabbitTemplate(ConnectionFactory factory) {
        TestRabbitTemplate template = new TestRabbitTemplate(factory);
        template.setMessageConverter(messageConverter());
        return template;
    }

    @Bean
    PDFGenerator pdfGenerator() throws IOException {
        String generatedOffersDit = "src/test/pdf_data/";
        if (!Files.exists(Path.of(generatedOffersDit))) {
            Files.createDirectory(Path.of(generatedOffersDit));
        }
        return new PDFGenerator( "/templates/cp_template.pdf",
                "/fonts/LiberationSansRegular.ttf",
                                 generatedOffersDit, 18);
    }

    @Bean
    Sender sender() {
        return Mockito.mock(Sender.class);
    }

    @Bean
    ErrorsResponseMessages errorsResponseMessage() {
        return new ErrorsResponseMessages("file", "db");
    }

    @Bean
    ExecutorService generatorPool() {
        return Executors.newFixedThreadPool(6);
    }

    @Bean
    public SimpleRabbitListenerContainerFactory rabbitListenerContainerFactory(ConnectionFactory mockConnectionFactory) {
        SimpleRabbitListenerContainerFactory factory = new SimpleRabbitListenerContainerFactory();
        factory.setConnectionFactory(mockConnectionFactory);
        factory.setMessageConverter(messageConverter());
        return factory;
    }
}
