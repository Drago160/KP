FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR=/service_root

RUN mkdir ${SERVICE_DIR}
COPY . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN pip3 install "."

CMD ["python3", "-u", "src/customer_creator/main.py"]
#CMD ["pytest"]  # for testing
