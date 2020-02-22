FROM python:3.7.6-slim

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY constants.py .
COPY schemas.py .
COPY services.py .

COPY config.yml .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh .
RUN chmod +x run.sh

CMD ./run.sh
