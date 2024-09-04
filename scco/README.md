# Work with project

## Structure

At first, some common things for all microservices:
- All microservices contain [`Dockerfile`](https://docs.docker.com/reference/dockerfile/).
- [`docker-compose`](https://docs.docker.com/compose/) is used for building and managing containers.
- [`RabbitMQ`](https://www.rabbitmq.com/) is used for microservices communication.
- All messages have `JSON` format. API of each service and json structure is located in its `README.md`.
- Services know queues of each other by data located in `.env`. Exactly:
  ```bash
  SERVICE_FOLDER="name_of_service"
  SERVICE_EXCHANGE="..."
  SERVICE_QUEUE="..."
  SERVICE_ROUTING_KEY="..."
  ```
- Checklist on `docker` and `docker-compose` usage (regardless of that project) can be found in `docs/docker_checklist.md`.
- Default settings (will appear in text below) in most cases can be changed by editing `.env`.


Each folder is a separate microservice and can be managed independently of others. To connect services to already existing `RabbitMQ`, volumes and other services, one have to edit `Set up on server` section in `.env`.

To ease development and creation of new services, there are several [docker-compose profiles](https://docs.docker.com/compose/profiles/) in `docker-compose`. Among them:
- `prod` (default) &mdash; all completed services, required for application.
- `crud` &mdash; database service (`db_functional_service`) and its dependencies.

There are three `docker-compose` config files:
- `docker-compose.yml` (default) &mdash; for local debug/test/release run.
- `docker-compose_services.yml` &mdash; build images on CI.
- `docker-compose._all.yml` &mdash; start services from prepared images.

## Prerequisites

To correct work of services you have to set up the following things:
1) Create `scco/db_functional_service/.env.secret.postgres`. It should contain the following data:
   ```text
   POSTGRES_USER=scco_postgres
   POSTGRES_PASSWORD=scco_password
   POSTGRES_PORT=5432
   POSTGRES_DB=scco_db
   ```
   For local testing you can specify arbitrary values.

2) Up container with `rabbitmq` from `tests/outside` (folder above). **All you need is RabbitMQ, other services were used for testing**.

3) Add api tokens to `ml_generation` service. See `Files With Secrets` in [README.md](ml_generation/ml_models/README.md) of that service.

4) Create required docker volumes. From project root run `setup.sh`:
   ```bash
   sudo ./setup.sh
   sudo ./setup.sh -e # to make external to project volumes (parser_bot_csv)
   sudo ./setup.sh -r # recreate volumes
   ```
   Volumes will bw created in `volumes` folder in the project root.

### Starting and stopping of microservices

1) Go to `scco` folder and run:
   ```bash
   # start
   docker-compose up --build -d
   # stop
   docker-compose down
   docker-compose down --remove-orphans # remove containers
   docker-compose down --remove-orphans --volumes # remove volumes for postgres
   docker-compose down --remove-orphans --volumes --rmi all # remove all images
   ```

2) Copy some data from `tests/data` folder to `volumes/parser_bot_csv`. In that tutorial we will copy `it/outstaffing_409` and `builder/stroiteli_moskva_1000.csv`.

3) Send to `scco_debug_customer_creator` queue new customers (see [README.md](customer_creator/README.md) for API). We will insert `customer_it` and `customer_builder`.

4) Send to `scco_debug_data_preprocessing ` messages:
   ```json
   {
     "customer_id": "customer_it",
     "parsed_csv": "it/outstaffing_409"
   }
   ```
   ```json
   {
     "customer_id": "customer_builder",
     "parsed_csv": "builder/stroiteli_moskva_1000.csv"
   }
   ```

5) Generated CO will be located in `volumes/generated_offers`. In addition, there is `volumes/unprocessed_parser_bot_csv` folder, which contains `csv` files with new messages (they are generated be `data_preprocessing` service).

## Debug

### Starting and stopping specific services

1) Run `db_functional_service` to enable database interaction:
   ```bash
   # start
   docker-compose --profile crud up --build -d
   # stop
   docker-compose --profile crud down --remove-orphans
   docker-compose --profile crud down --remove-orphans --volumes # delete postgres volume
   ```

2) Run specific service `<service_name>`:
   ```bash
   # run
   docker-compose up --build -d <service_name>
   # stop
   docker-compose stop <service_name>
   docker-compose rm <service_name> # remove container
   docker-compose rmi <service_name> # remove image
   ```


## Queries to database
For arbitrary queries you have to up `pgadmin_fs` service:
```bash
docker-compose up --build -d pgadmin_fs
```
And follow instruction in [README.md](./db_functional_service/README.md) of `db_functional_service`.


## Bugs
- `db_functional_service` has callback `filter_new_queries`. It is used by `data_preprocessing` and creates only one query to database. For now `data_preprocessing` send data about all client messages in one query, therefore `csv` files that contain a lot of rows (validated on 10000), leads for `db_functional_service` to crash. To avoid that problem, send to `data_preprocessing` only those `csv` files that contain no more than 1000 rows.

# Notes

`POSTGRES_HOST` must be the same as the service name or network alias in `docker compose`.

After several launches, you may have a lot of "hanging" images that will take up memory. To **delete hanging images** use the command:
```bash
docker images -f dangling=true # show list of dangling images
docker rmi $(docker images -f dangling=true -q)
docker image prune # shorter version
```

**Removing containers**:
```bash
# Удаление всех остановленных контейнеров.
docker container prune
# Удаление всех <none> контейнеров.
docker ps -a | grep '<none>' | awk '{ print $1; }' | xargs docker rm
```
