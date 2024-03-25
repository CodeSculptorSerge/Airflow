FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/output_data && \
    chmod 755 /app/output_data

USER appuser
