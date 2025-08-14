FROM python:3.11
RUN mkdir -p /app
WORKDIR /app
COPY src/ /app
COPY requirements.txt requirements-mariadb.txt /
RUN python3 -m venv /venv && \
    /venv/bin/pip3 install --upgrade pip && \
    /venv/bin/pip3 install -r /requirements-mariadb.txt
CMD ["/venv/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app"]
