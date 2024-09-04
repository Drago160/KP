#!/bin/bash

# -p | --project-root --- path to project root ($CI_PROJECT_ROOT in gitlab)
# -s | --service-name --- name of service to build

################################################################################

# Script.
SERVICE_NAME=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    -p|--project-root)
      PROJECT_ROOT="$2" #
      echo "Project directory: ${PROJECT_ROOT}"
      shift 2 ;;
    -s|--service-name)
      SERVICE_NAME="$2"
      shift 2 ;;
    *)
      echo "Unexpected argument: '$1'"
      exit 1
  esac
done

if [ -z "${PROJECT_ROOT}" ]; then
  echo "-p is not set, set PROJECT_ROOT=."
  PROJECT_ROOT="."
fi

if [ -z "${SERVICE_NAME}" ]; then
  echo "-s (service name) is required, but not provided"
  PROJECT_ROOT="."
fi

echo "cd to PROJECT_ROOT"
cd "${PROJECT_ROOT}"

################################################################################

# Services
ENV_FILE="./scco/.env"
set -o allexport
source "${ENV_FILE}" set
set +o allexport
echo ${PDF_GENERATION_EXCHANGE}


if [ "${SERVICE_NAME}" = "data_preprocessing" ]; then
  docker build -t scco_test_data_preprocessing "./scco/data_preprocessing"
  docker run --name scco_test_data_preprocessing --env-file ./scco/.env scco_test_data_preprocessing python3 run_tests.py
  docker rm scco_test_data_preprocessing
elif [ "${SERVICE_NAME}" = "ml_generation" ]; then
  docker build -t scco_test_ml_generation "./scco/ml_generation"
  docker run --name scco_test_ml_generation scco_test_ml_generation pytest
  docker rm scco_test_ml_generation
elif [ "${SERVICE_NAME}" = "pdf_generation" ]; then
  docker build -t scco_test_pdf_generation -f ./scco/pdf_generation/TestDockerfile "./scco/pdf_generation"
  docker run --name scco_test_pdf_generation scco_test_pdf_generation
  docker rm scco_test_pdf_generation

elif [ "${SERVICE_NAME}" = "db_functional_service" ]; then
  docker build -t scco_test_db_functional_service "./scco/db_functional_service"
  docker run --name scco_test_db_functional_service scco_test_db_functional_service pytest
  docker rm scco_test_db_functional_service
else
  echo "Unknown service name: ${SERVICE_NAME}"
fi
