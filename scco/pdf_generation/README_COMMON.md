Сервис постобработки читает из rabbit информацию о КП: id КП, текст, сгенерированного КП и текст с контактной информацией заказчика.

### Пайплайн:

1. Чтение из сообщения из rabbit в методе consume класса Receiver
2. Постобработка через ProcessingChain
3. Генерация pdf в PdfGenerator
4. Сохранение файла на сервер
5. Вставка в БД в методе sendCPToDB класса Sender
6. Получение ответа БД в методе consumeDBResponse класса Receiver
7. Отправка сообщения из приложения в sendCPToOutput класса Sender

### Постобработка:

1. удаление указаний имени по паттерну "Меня зовут"/"Мое имя"
2. удаление предложений в последних 30% текста, содержащих "С уважением"
3. удаление предложений, содержащих квадратные скобок \[ ].

Все классы постобработки находятся в пакете processors (scco/pdf_generation/src/main/java/ru/scco/pdf_generator/processors) Там же есть README.md с описанием организации пайплайна постобработки.

### Генерация pdf

PdfGenerator заполняет в шаблоне поле main_text текстом кп и контактной информацией. Если текст переполняет поле, страница шаблона копируется и заполнение продолжается.

#### **Pdf-шаблон:**

Pdf-шаблон, имеет следующий формат: одна страница с одной текстовой формой (text box), имеющей имя main_text

Шаблон хранится resources/templates (scco/pdf_generation/src/main/resources/templates)

Сейчас используется cp_template.pdf. Название регулируется в application. properties

Шаблон с формой можно создать в специализированных pdf-редакторах (Например, в libreoffice draw через insert->form control->text box) или можно добавить форму к существующему pdf (Например, в [https://www.sejda.com/pdf-forms](https://www.sejda.com/pdf-forms) через text_area)

#### Шрифт

Из поля main_text берется информации о размере поля текста, размере шрифта, цвете, но не о самом шрифте.

Шрифт берется из resources/fonts (scco/pdf_generation/src/main/resources/fonts)

Сейчас используется LiberationSansRegular.ttf. Название шрифта регулируется в application.properties.



### Запись файла

Сгенерированный pdf сохраняется как  ${GENERATED_OFFERS_VOLUME_PATH}/message_group_id.pdf, где ${GENERATED_OFFERS_VOLUME_PATH} указан в .env, message_group_id - id сгенерированного КП, который  сервис получает вместе с текстом КП



