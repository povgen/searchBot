### Описание
Бот занимается поиском объявление на KupajemProdajem по запросу на русском языке, 
автоматически переводя его на сербский язык выводя пользователю объявления переведенные 
с сербского языка 

### Запуск:
- С помощью бота https://t.me/BotFather в телеграмме создайте своего бота
- Скопируйте/переименуйте файл template.env в .env
- В переменную API_TOKEN положите токен вашего бота 
#### Через docker:
- Опционально можете добавить volumes, для дампа redis (/data) и для логов бота (/app/logs)
```yaml
version: "3.7"
services:
  redis:
    image: redis:latest
    expose:
      - 6379
    volumes:
      - /your_directory:/data

  app:
    build: .
    container_name: search_bot
    env_file:
      - .env
    depends_on:
      - redis
    volumes:
      - /your_directory:/app/logs

```
- Запустите контейнеры выполнив следующую команду
```shell
 docker compose up
```
#### Если docker'а нет:
- Установите redis https://redis.io/docs/getting-started/installation/install-redis-on-windows/
- Подправьте .env файл указав туда в соответствующие переменные хост (localhost) и порт redis
- Для работы Selenium, необходимо иметь установленный браузер Chrome или firefox, если у вас второе то так же подправьте .env: SELENIUM_BROWSER=firefox
- выполните команду
```shell
 py main.py
```
____
в файле logs/log.log хранятся логи работы бота
в файле logs/feedback.txt хранятся обратная связь от пользователей 
____
Запуск редиса
```shell
docker run --name some-redis -d -p 6379:6379 -rm redis
```