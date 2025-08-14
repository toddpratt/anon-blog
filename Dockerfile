FROM python:3.11
RUN mkdir -p /work
WORKDIR /work
COPY src /work/app
COPY requirements.txt requirements-mariadb.txt /work
RUN python3 -m venv /venv && \
    /venv/bin/pip3 install --upgrade pip && \
    /venv/bin/pip3 install gunicorn && \
    /venv/bin/pip3 install -r /work/requirements-mariadb.txt
CMD ["/venv/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app"]
