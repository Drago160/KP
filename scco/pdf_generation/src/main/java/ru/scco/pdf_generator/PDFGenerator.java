package ru.scco.pdf_generator;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.cos.COSDictionary;
import org.apache.pdfbox.io.IOUtils;
import org.apache.pdfbox.multipdf.LayerUtility;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.PDPageTree;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDFont;
import org.apache.pdfbox.pdmodel.font.PDType0Font;
import org.apache.pdfbox.pdmodel.graphics.form.PDFormXObject;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotation;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotationWidget;
import org.apache.pdfbox.pdmodel.interactive.form.PDAcroForm;
import org.apache.pdfbox.pdmodel.interactive.form.PDTextField;

import java.awt.geom.AffineTransform;
import java.io.IOException;
import java.nio.file.Path;
import java.util.*;

// This class is responsible for inserting text in pdf-template and saving at the server
@Slf4j
@RequiredArgsConstructor
public class PDFGenerator {
    private final String templatePath;
    private final String fontPath;
    private final String destinationPath;
    private final int defaultFontSize;

    // Connection with page may not know about its page,
    // But page has to know about widgets
    // Method finds page that contains certain widget
    private static PDPage getPdPage(PDDocument document,
                                    PDAnnotationWidget widget)
            throws IOException {
        PDPage page = widget.getPage();
        if (page == null) {
            PDPageTree pages = document.getPages();
            for (int i = 0; i < pages.getCount(); ++i) {
                for (PDAnnotation annotation : pages.get(i).getAnnotations()) {
                    COSDictionary annotationObject = annotation.getCOSObject();
                    if (annotationObject.equals(widget.getCOSObject())) {
                        page = pages.get(i);
                        i = pages.getCount();
                        break;
                    }
                }
            }
        }
        return page;
    }

    // This method is responsible for wrapping long lines
    // If text does not fit rectangle's size, method returns rest of the text
    // This method reads text char by char, tries to wrap text by space
    private static String showLongLine(String text,
                                       PDPageContentStream contentStream,
                                       PDFont font, int fontSize,
                                       PDRectangle rectangle)
            throws IOException {
        float deltaY = -fontSize * (font.getBoundingBox()
                                        .getHeight()) / 1000;
        contentStream.newLineAtOffset(0, deltaY);
        rectangle.setUpperRightY(rectangle.getUpperRightY() + deltaY);

        // Text that definitely will be shown
        StringBuilder lineBuilder = new StringBuilder();
        // One word. Will be merged with lineBuilder when separate will be found
        // If length of wordBuilder passes width of rectangle, it word be shown
        StringBuilder wordBuilder = new StringBuilder();
        float lineOffset = 0; // size of lineBuilder in pdf
        float wordOffset = 0; // size of wordBuilder in pdf

        for (int i = 0; i < text.length(); i++) {
            if (rectangle.getHeight() <= 0) {
                return wordBuilder.append(text.substring(i)).toString();
            }
            float charLength =
                    font.getStringWidth("" + text.charAt(i)) * fontSize / 1000;
            if (lineOffset + wordOffset + charLength
                > rectangle.getUpperRightX() - rectangle.getLowerLeftX()) {
                if (!lineBuilder.isEmpty()) {
                    contentStream.showText(lineBuilder.toString());
                    lineBuilder = new StringBuilder();
                    lineOffset = 0;
                } else {
                    contentStream.showText(wordBuilder.toString());
                    wordBuilder = new StringBuilder();
                    wordOffset = 0;
                }
                contentStream.newLineAtOffset(0, deltaY);
                rectangle.setUpperRightY(rectangle.getUpperRightY() + deltaY);
            }
            wordBuilder.append(text.charAt(i));
            wordOffset += charLength;
            if (text.charAt(i) == ' ') {
                lineOffset += wordOffset;
                wordOffset = 0;
                lineBuilder.append(wordBuilder);
                wordBuilder = new StringBuilder();
            }
        }
        contentStream.showText(lineBuilder.append(wordBuilder).toString());
        contentStream.newLineAtOffset(0, deltaY);
        rectangle.setUpperRightY(rectangle.getUpperRightY() + deltaY);
        return "";
    }


    // create stream on the particular page by field.
    // Content stream does not return information about its settings,
    // such as font or fontsize, so fontSize is also return from the method
    private Map.Entry<PDPageContentStream, Integer> initContentStream(
            PDDocument document,
            PDPage page,
            PDTextField field,
            PDFont font)
            throws IOException {
        PDPageContentStream contentStream =
                new PDPageContentStream(document, page,
                                        PDPageContentStream.AppendMode.APPEND,
                                        false, true);
        int fontSize = setAppearance(contentStream,
                                     field.getDefaultAppearance(), font);
        contentStream.beginText();
        contentStream.newLineAtOffset(
                field.getWidgets().get(0).getRectangle().getLowerLeftX(),
                field.getWidgets().get(0).getRectangle().getUpperRightY());
        return Map.entry(contentStream, fontSize);
    }

    // parse appearance to customize contentStream
    private int setAppearance(PDPageContentStream contentStream,
                              String appearance, PDFont font)
            throws IOException {
        int fontSize = this.defaultFontSize;
        if (appearance != null) {
            String[] styleSettings = appearance.split(" ");
            if (styleSettings.length == 7) {
                fontSize = Integer.parseInt(styleSettings[1]);
                contentStream.setNonStrokingColor(
                        Float.parseFloat(styleSettings[3]),
                        Float.parseFloat(styleSettings[4]),
                        Float.parseFloat(styleSettings[5]));
            }
        }
        contentStream.setFont(font, fontSize);
        return fontSize;
    }


    private String fillMultiPageTemplate(long messageID,
                                         String mainText) {
        try (PDDocument doc =
                     Loader.loadPDF(IOUtils.toByteArray(Objects.requireNonNull(
                             PDFGenerator.class.getResourceAsStream(
                                     templatePath)))
                     )) {
            // Load font that supports non-ascii symbols
            PDFont font = PDType0Font.load(
                    doc, PDFGenerator.class.getResourceAsStream(fontPath),
                    false);

            // Load form and its rectangle (coordinates)
            PDAcroForm acroForm = doc.getDocumentCatalog().getAcroForm();
            PDTextField inputField =
                    (PDTextField) acroForm.getField("main_text");
            PDRectangle inputRectange =
                    inputField.getWidgets().get(0).getRectangle();

            PDPage page = doc.getPage(0);

            // Init layer utility and load page as form in order to
            // match its template when creating new pages
            LayerUtility layerUtility = new LayerUtility(doc);
            PDFormXObject pageTemplate =
                    layerUtility.importPageAsForm(doc, 0);
            AffineTransform affineTransform = new AffineTransform();

            Map.Entry<PDPageContentStream, Integer> streamInfo =
                    initContentStream(doc, page, inputField, font);
            PDPageContentStream contentStream = streamInfo.getKey();
            int fontSize = streamInfo.getValue();

            int pageIndex = 0;
            Deque<String> lines =
                    new ArrayDeque<>(Arrays.asList(mainText.split("\n")));
            // write line by line. If text does not fit form size,
            // new page and content stream are created
            while (!lines.isEmpty()) {
                String restText =
                        showLongLine(lines.removeFirst(),
                                     contentStream, font,
                                     fontSize,
                                     inputRectange);
                if (inputRectange.getHeight() <= 0) {
                    contentStream.endText();
                    contentStream.close();
                    page = new PDPage(page.getMediaBox());
                    doc.addPage(page);
                    layerUtility.appendFormAsLayer(page, pageTemplate,
                                                   affineTransform,
                                                   "page" + pageIndex);
                    pageIndex++;
                    streamInfo = initContentStream(doc, page, inputField, font);
                    contentStream = streamInfo.getKey();
                    fontSize = streamInfo.getValue();
                    inputRectange =
                            inputField.getWidgets().get(0).getRectangle();
                    lines.addFirst(restText);
                }
            }

            contentStream.endText();
            contentStream.close();

            // Close template's form. It will become a regular widget at the
            // behind the text.
            acroForm.flatten();
            Path filePath = Path.of(destinationPath, messageID + ".pdf");
            doc.save(filePath.toAbsolutePath().toString());
            return filePath.getFileName().toString();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public String generate(long messageId, String cp, String contactInfo) {
        return fillMultiPageTemplate(messageId, cp + "\n" + contactInfo);
    }
}