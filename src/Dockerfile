FROM python:3.11.3

WORKDIR ./app

COPY Application .

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT bash run_server.sh