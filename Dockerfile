FROM python:3.11
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .
RUN python3 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt
CMD ["venv/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app"]
