# README_BUILDING

В репозитории есть 2 dockerfile: Dockerfile - для запуска сервиса, TestDockerfile - для запуска тестов.

Вообще говоря ничего в ручную запускать не нужно. Запуск сервисов через docker compose см в README в /scco, запуск тестов через скрипт см README в /tests/ci

Если все же нужно запустить отдельно:

Для корректной работы тестов нужно передать .env файл

Для корректного запуска сервиса нужно передать .env файл и развернуть кролика (последнее см README в tests/outside)

Пример запуска тестов:

```bash
docker build -t scco_test_pdf_generation -f ./scco/pdf_generation/TestDockerfile ./scco/pdf_generation/
docker run --env-file ./scco/.env scco_test_pdf_generation
```

