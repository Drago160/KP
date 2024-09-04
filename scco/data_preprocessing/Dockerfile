FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR=/data_preprocessing

RUN mkdir ${SERVICE_DIR}
COPY ./requirements.txt ${SERVICE_DIR}/
WORKDIR ${SERVICE_DIR}

RUN pip3 install -r requirements.txt

COPY . ${SERVICE_DIR}

CMD python3 data_preprocessing.py
# CMD python3 data_preprocessing.py > /dev/null
