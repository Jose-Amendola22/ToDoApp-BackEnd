# Docker file FOR TORNADOPY API!
FROM python:3.9-slim

WORKDIR /app

COPY app/ .

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

CMD ["python", "main.py"]
