import re

from googletrans import Translator


def translate_to_ru(text):
    translator = Translator()
    result = translator.translate(text, src='sr', dest='ru')
    return result.text


def translate_to_sr(text):
    searched = re.findall('[A-z]+', text)
    parts = re.split('[A-z]+', text)
    res = []
    translator = Translator()

    for index, part in enumerate(parts):
        if part.strip():
            res.append(translator.translate(part, src='ru', dest='sr').text)
        if index < len(searched):
            res.append(searched[index])

    return ' '.join(res)
