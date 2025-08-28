FROM python:3.11
RUN mkdir -p /app
WORKDIR /app
COPY abapi/ /app/
COPY migrations /app/migrations/
COPY entrypoint.sh requirements.txt requirements-db.txt /
RUN python3 -m venv /venv && \
    /venv/bin/pip3 install --upgrade pip && \
    /venv/bin/pip3 install -r /requirements.txt && \
    /venv/bin/pip3 install -r /requirements-db.txt && \
    chmod +x /entrypoint.sh
CMD ["/entrypoint.sh", "-b", "0.0.0.0:5000", "app:app"]
