#!/bin/bash

# -p | --project-root --- path to project root ($CI_PROJECT_ROOT in gitlab)
# -s | --service-name --- name of service to build
# -i | --image-name --- name of result image

################################################################################

# Script.
SERVICE_NAME=""
IMAGE_NAME=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    -p|--project-root)
      PROJECT_ROOT="$2" #
      echo "Project directory: ${PROJECT_ROOT}"
      shift 2 ;;
    -s|--service-name)
      SERVICE_NAME="$2"
      shift 2 ;;
    -i|--image-name)
      IMAGE_NAME="$2"
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

if [ -z "${IMAGE_NAME}" ]; then
  echo "-i (image name) is required, but not provided"
  PROJECT_ROOT="."
fi

echo "cd to PROJECT_ROOT"
cd "${PROJECT_ROOT}"
ENV_FILE="./scco/.env"
cat ${ENV_FILE}
set -o allexport
source "${ENV_FILE}" set
set +o allexport
echo ${PDF_GENERATION_FOLDER}

################################################################################

# Build images
# shellcheck disable=SC2046
if [ "${SERVICE_NAME}" = "data_preprocessing" ]; then
  docker build -t "${IMAGE_NAME}" "scco/data_preprocessing"
elif [ "${SERVICE_NAME}" = "ml_generation" ]; then
  docker build -t "${IMAGE_NAME}" "scco/ml_generation"
elif [ "${SERVICE_NAME}" = "pdf_generation" ]; then
  docker build -t "${IMAGE_NAME}" "scco/pdf_generation"
elif [ "${SERVICE_NAME}" = "db_functional_service" ]; then
  docker build -t "${IMAGE_NAME}" "scco/db_functional_service"
else
  echo "Unknown service name: ${SERVICE_NAME}"
fi
