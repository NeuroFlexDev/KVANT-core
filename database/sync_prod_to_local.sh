#!/usr/bin/env bash
set -euo pipefail

# This script copies the production database into a local development instance
# without touching production state. It performs a pg_dump from the prod server
# and restores it into the locally running postgres (default: kvant_dev on localhost:5432).
#
# Usage:
#   export PROD_DB_HOST=...
#   export PROD_DB_PORT=...
#   export PROD_DB_NAME=...
#   export PROD_DB_USER=...
#   export PROD_DB_PASSWORD=...
#   export LOCAL_DB_HOST=localhost
#   export LOCAL_DB_PORT=5432
#   export LOCAL_DB_NAME=kvant_dev
#   export LOCAL_DB_USER=kvant_user
#   export LOCAL_DB_PASSWORD=kvant_password
#   ./sync_prod_to_local.sh

required_vars=(
  PROD_DB_HOST
  PROD_DB_PORT
  PROD_DB_NAME
  PROD_DB_USER
  PROD_DB_PASSWORD
  LOCAL_DB_HOST
  LOCAL_DB_PORT
  LOCAL_DB_NAME
  LOCAL_DB_USER
  LOCAL_DB_PASSWORD
)

RESTORE_FILTER_REGEX="${RESTORE_FILTER_REGEX:-^SET transaction_timeout =}"
if [[ -n "${RESTORE_FILTER_REGEX}" ]]; then
  RESTORE_FILTER_CMD=(sed -e "/${RESTORE_FILTER_REGEX}/d")
else
  RESTORE_FILTER_CMD=(cat)
fi

set_pg_ssl_env() {
  local mode="$1"
  local cert="$2"

  if [[ -n "${mode:-}" ]]; then
    export PGSSLMODE="$mode"
  else
    unset PGSSLMODE
  fi

  if [[ -n "${cert:-}" ]]; then
    export PGSSLROOTCERT="$cert"
  else
    unset PGSSLROOTCERT
  fi
}

for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "Error: environment variable $var is not set" >&2
    exit 1
  fi
done

echo "Starting production database dump..."
export PGPASSWORD="${PROD_DB_PASSWORD}"
set_pg_ssl_env "${PROD_DB_SSLMODE:-}" "${PROD_DB_SSLROOTCERT:-}"
pg_dump \
  --no-owner \
  --no-privileges \
  --format=custom \
  --host="${PROD_DB_HOST}" \
  --port="${PROD_DB_PORT}" \
  --username="${PROD_DB_USER}" \
  "${PROD_DB_NAME}" \
  > /tmp/kvant_prod.dump

echo "Dropping and recreating local database schema..."
export PGPASSWORD="${LOCAL_DB_PASSWORD}"
set_pg_ssl_env "${LOCAL_DB_SSLMODE:-}" "${LOCAL_DB_SSLROOTCERT:-}"
psql \
  --host="${LOCAL_DB_HOST}" \
  --port="${LOCAL_DB_PORT}" \
  --username="${LOCAL_DB_USER}" \
  --dbname=postgres \
  --command="DROP DATABASE IF EXISTS \"${LOCAL_DB_NAME}\";"

psql \
  --host="${LOCAL_DB_HOST}" \
  --port="${LOCAL_DB_PORT}" \
  --username="${LOCAL_DB_USER}" \
  --dbname=postgres \
  --command="CREATE DATABASE \"${LOCAL_DB_NAME}\" OWNER \"${LOCAL_DB_USER}\";"

echo "Restoring dump into local database..."
set_pg_ssl_env "${LOCAL_DB_SSLMODE:-}" "${LOCAL_DB_SSLROOTCERT:-}"
pg_restore \
  --no-owner \
  --no-privileges \
  --clean \
  --if-exists \
  --file=- \
  /tmp/kvant_prod.dump \
  | "${RESTORE_FILTER_CMD[@]}" \
  | psql \
      --host="${LOCAL_DB_HOST}" \
      --port="${LOCAL_DB_PORT}" \
      --username="${LOCAL_DB_USER}" \
      --dbname="${LOCAL_DB_NAME}" \
      --set=ON_ERROR_STOP=on \
      --single-transaction

echo "Cleaning up temporary dump..."
rm -f /tmp/kvant_prod.dump

echo "Local database has been synchronized with production snapshot."
