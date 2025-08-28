#! /bin/sh

echo "[Init] Waiting for DB creds... (${CREDENTIALS_FILE})"
until [ -f "${CREDENTIALS_FILE}" ]; do
  sleep 1
done

/venv/bin/flask db upgrade

/venv/bin/gunicorn "$@"
