import json

from settings import r


async def get_cached_data(url: str, get_data: callable, hook_get_data: callable = None) -> list or dict:
    """
    Метод для кэширования запросов
    url - запрос для получения данных,
    get_data - функция для получения данных, в случае их отсутствия в кэше
    """

    data = r.get(url)

    if data is None:
        data = await get_data(url)
        r.set(url, json.JSONEncoder().encode(data))
        r.expire(url, 60 * 60 * 24)
        if hook_get_data is not None:
            hook_get_data()
    else:
        data = json.JSONDecoder().decode(data)

    return data


def splice_text_by_parts(text, max_part_len=4000):
    text_parts = []

    while len(text) > max_part_len - 200:
        # если пробельный символ не будет найден, то просто поделим по максимально допустимой длине
        split_index = max_part_len

        # ищем ближайший пробел, по которому разделим текст
        for i in range(max_part_len - 200, max_part_len):
            if text[i] == ' ':
                split_index = i
                break

        # добавляем тест в части текста
        text_parts.append(text[:split_index])

        # удаляем из текста отделенную часть
        text = text[split_index:]

    # если в тесте остались символы так же добавим его в text_parts
    if text.strip() != '':
        text_parts.append(text)

    return text_parts


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


def var_dump(variable, indent=0, padding=4):
    indentation = " " * indent

    if isinstance(variable, (list, tuple)):
        result = [var_dump(item, indent + padding, padding) for item in variable]
        return '\n' + (',\n'.join(result)) + '\n' + indentation

    if isinstance(variable, dict):
        result = []
        for key, value in variable.items():
            value_str = var_dump(value, indent + padding, padding)
            result.append(f'{indentation}{key}: {value_str}')
        return '\n'+(',\n'.join(result))

    return repr(variable)
