package ru.scco.pdf_generator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PDFEntrypoint {
    public static void main(String[] args) {
        SpringApplication.run(PDFEntrypoint.class, args);
    }
}