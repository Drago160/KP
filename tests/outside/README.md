# Поднятие кролика локально для тестирования

## Запуск и остановка `RabbitMQ`

Нужно перейти в папку `rabbitmq` и выполнить:
```bash
# run
docker-compose --env-file ../.env up --build -d
# stop
docker-compose --env-file ../.env down --remove-orphans --volumes
```
Достаточно один раз запустить контейнер, после чего он будет постоянно работать и при перезапуске системы автоматически запускаться (так работают все сервисы в docker-compose). Если в вашем сервисе возникает ошибка `Unexpected error: [Errno -3] Temporary failure in name resolution`, то скорее всего вы неправильно используете переменные окружения, которые отвечают за кролика (`RMQ_NET_ALIAS`, например).

# Оффтоп

## Стягивание папки `outside`
Из корня проекта выполнить команду:
```bash
git restore --source=SCCO-46-outside_rabbitmq --worktree outside
```

## Доступные сервисы
* `client_queries` - сервис, который отвечает за бота, от которого мы получаем `csv` файл с информацией.
* `generated_offers` - сервис, которому мы отправляем сгенерированный pdf файл.
* `rabbitmq` - брокер

## Запуск и остановка сторонних сервисов
Из папки `outside` нужно выполнить:
```bash
# start
docker-compose up --build -d
# stop
docker-compose down --rmi all --remove-orphans
```

Запуск отдельных сервисов. Из папки `outside` нужно выполнить:
```bash
# start
docker-compose --profile queries up -d
docker-compose --profile offers up -d
# stop
docker-compose --profile queries down --rmi all --remove-orphans
docker-compose --profile offers down --rmi all --remove-orphans
```

### Удаление контейнеров и образов связанных с `scco` вручную
```bash
./clear_docker.sh
```
