#!/bin/bash

# -e | --external --- build external volumes/objects/...
# -r | --recreate --- recreate volumes

PROJECT_DIR=$(dirname "$(realpath "$0")")

echo "Project directory: ${PROJECT_DIR}"

################################################################################

# User data (EDIT MANUALLY FOR EACH PROJECT).

read -r -d '' ENV_FILES<<'EOF' || echo "ok" > /dev/null
    scco/.env
EOF

################################################################################

# Script.
RECREATE=""
EXTERNAL=""

ENV_FILES=$(echo "${ENV_FILES}" | awk '{ print $1 }')

while [ "$#" -gt 0 ]; do
  case "$1" in
    -e|--external)
      EXTERNAL="1"
      shift 1 ;;
    -r|--recreate)
      RECREATE="1"
      shift 1 ;;
    *)
      echo "Unexpected argument: '$1'"
      exit 1
  esac
done

set -o allexport
for ENV_FILE in ${ENV_FILES}; do
  source "${PROJECT_DIR}/${ENV_FILE}" set
done
set +o allexport

################################################################################

# Volumes

function create_volume() {
  local VOLUME_NAME="$1"
  local VOLUME_FOLDER="$2"

  if [ -n "${RECREATE}" ]; then
    VOLUME_EXIST=$(docker volume ls -f name="^${VOLUME_NAME}\$")
    if [ -n "${VOLUME_EXIST}" ]; then
      echo -n "removing "
      docker volume rm "${VOLUME_NAME}"
    fi
    if [ -d "${VOLUME_FOLDER}" ]; then
      rm -rf "${VOLUME_FOLDER}"
    fi
  fi

  mkdir -p "${VOLUME_FOLDER}"
  echo -n "creating "
  docker volume create --driver local \
        --name "${VOLUME_NAME}" \
        --opt type=volume \
        --opt o=bind \
        --opt device="${VOLUME_FOLDER}"
}

# parser_bot_csv
if [ -n "${EXTERNAL}" ]; then
  VOLUME_FOLDER="${PROJECT_DIR}/volumes/parser_bot_csv"
  create_volume "${PARSER_BOT_CSV_VOLUME_NAME}" "${VOLUME_FOLDER}"
fi

# unprocessed_parser_bot_csv
VOLUME_FOLDER="${PROJECT_DIR}/volumes/unprocessed_parser_bot_csv"
create_volume "${UNPROCESSED_PARSER_BOT_CSV_VOLUME_NAME}" "${VOLUME_FOLDER}"

# generated_offers
VOLUME_FOLDER="${PROJECT_DIR}/volumes/generated_offers"
create_volume "${GENERATED_OFFERS_VOLUME_NAME}" "${VOLUME_FOLDER}"
