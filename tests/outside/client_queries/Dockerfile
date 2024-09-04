FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR=/service_root

RUN mkdir ${SERVICE_DIR}
COPY . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN pip3 install -r ${SERVICE_DIR}/requirements.txt

CMD ["python3", "-u", "src/main.py"]
