import json

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


async def get_cached_data(url: str, get_data: callable) -> list or dict:
    """
    Метод для кэширования запросов
    url - запрос для получения данных,
    get_data - функция для получения данных, в случае их отсутствия в кэше
    """

    data = r.get(url)

    if data is None:
        data = await get_data(url)
        r.set(url, json.JSONEncoder().encode(data))
        r.expire(url, 60*60*24)
    else:
        data = json.JSONDecoder().decode(data)

    return data


class Store:
    """Используется, для работы с inlineButtons для передачи больших данных в обработчик"""
    cache: dict = {}

    def get_hash(self, data):
        """Сохраняем данные и получаем их хэш"""
        data_hash = str(hash(data))

        if data_hash not in self.cache:
            self.cache[data_hash] = data

        return data_hash

    def get_data(self, data_hash):
        """По хэшу получаем сохраненные ранее данные"""
        return None if data_hash not in self.cache else self.cache[data_hash]
