FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP worker
EXPOSE 5000
COPY entrypoint.sh entrypoint.sh
COPY worker worker

ENTRYPOINT ["./entrypoint.sh"]