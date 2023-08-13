FROM python:latest
LABEL authors="povgen"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


CMD ["python", "main.py"]