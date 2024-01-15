FROM --platform=linux/x86_64 python:3.10.4-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5757
COPY . .

ENV PYTHONUNBUFFERED=1

ENV POSTGRES_HOST postgis
ENV POSTGRES_PORT 5432
ENV POSTGRES_DB dotgis_ctc
ENV POSTGRES_USER postgres
ENV POSTGRES_PASS DOTGIS_2020

CMD ["python3", "main.py"]