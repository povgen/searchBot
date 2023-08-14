FROM python:latest
LABEL authors="povgen"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN ["chmod", "+x", "./docker/install_browser.sh"]
RUN ./docker/install_browser.sh

CMD ["python", "main.py"]
