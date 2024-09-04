FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR="/service_root"
ENV PYTHONUNBUFFERED="1"
ARG SERVICE_PACKAGE_NAME="db_functional_service"
ARG MAIN_FILE="main.py"

#SHELL ["/bin/bash", "-c"]

RUN mkdir ${SERVICE_DIR}
COPY . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

# Only install (flag -n)
RUN ["./run.sh", "-n"]

#CMD ["/bin/bash", "-c", "./run.sh -f ${MAIN_FILE}"]
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./run.sh -f src/service/main.py"]
#CMD ["pytest"]  # for testing

# Dependencies for psycopg2.
#RUN apt-get install \
#    libpq-dev \
#    libssl-dev \
#    libffi-dev \
#    python3-dev

#ENTRYPOINT ["python3", "-u"]
