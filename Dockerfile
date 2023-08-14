FROM python:latest
LABEL authors="povgen"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN ./docker/install_browser.sh

CMD ["python", "main.py"]
