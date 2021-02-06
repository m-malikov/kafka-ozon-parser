FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY entrypoint.sh entrypoint.sh
COPY parser parser

ENTRYPOINT ["./entrypoint.sh"]