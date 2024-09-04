#!/bin/bash

# -e --- editable install (debug)
# -r --- reinstall
# -f --- path to .py file to run (relative to package directory)
# -n --- don't run application
# -u --- uninstall package
# -h --- is on host

################################################################################

# User data (EDIT MANUALLY FOR EACH PROJECT).

#set -x # debug
#set -eu

read -r -d '' ENV_FILES<<'EOF' || echo "ok" > /dev/null
    ../.env
EOF

PACKAGE_NAME="customer_creator"

################################################################################

# Script.

REINSTALL=""
NOT_RUN=""
UNINSTALL=""
export IS_ON_HOST=""

ENV_FILES=$(echo "${ENV_FILES}" | awk '{ print $1 }')
PIP_INSTALL_ARGS="."
MAIN_FILE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    -e|--editable)
      PIP_INSTALL_ARGS="--editable ${PIP_INSTALL_ARGS}"
      shift 1 ;;
    -r|--reinstall)
      REINSTALL="1"
      shift 1 ;;
    -f|--file)
      MAIN_FILE="$2"
      shift 2 ;;
    -n|--not-run)
      NOT_RUN="1"
      shift 1 ;;
    -u|--uninstall)
      UNINSTALL="1"
      shift 1 ;;
    -h|--on-host)
      export IS_ON_HOST="true"
      shift 1 ;;
    *)
      echo "Unexpected argument: '$1'"
      exit 1
  esac
done

if [ -n "${UNINSTALL}" ]; then
  echo "Uninstalling package."
  pip3 uninstall -y "${PACKAGE_NAME}"
  exit 0
fi

if [ -z "${MAIN_FILE}" ]; then
  if [ -z "${NOT_RUN}" ]; then
    echo "-f option is omitted, but required to specify file"
    exit 1
  fi
fi

if [ -n "${REINSTALL}" ]; then
  echo "Uninstalling package."
  pip3 uninstall -y "${PACKAGE_NAME}"
  echo "Installing package."
  pip3 install ${PIP_INSTALL_ARGS}
else
  PACKAGE_IS_INSTALLED="$(pip3 freeze | grep "${PACKAGE_NAME}")"
  if [ -n "${PACKAGE_IS_INSTALLED}" ]; then
    echo "Package is already installed, skip installation."
  else
    echo "Installing package."
    pip3 install ${PIP_INSTALL_ARGS}
  fi
fi

#for ENV_FILE in ${ENV_FILES}; do
#  ENV_VARS="$(grep -Ev '^\s*#|^\s*$' "${ENV_FILE}" | xargs -d '\n')"
#  for ENV_VAR in ${ENV_VARS}; do
#    export "${ENV_VAR?}"
#  done
#done

set -o allexport
for ENV_FILE in ${ENV_FILES}; do
  source "${ENV_FILE}" set
done
set +o allexport

################################################################################

# Run.

if [ -z "${NOT_RUN}" ]; then
  echo -e "Run package main.\n-----------------------------------------------"
  python3 -u "src/${PACKAGE_NAME}/${MAIN_FILE}"
fi

