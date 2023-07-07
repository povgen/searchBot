from googletrans import Translator


def translate_to_ru(text):
    translator = Translator()
    result = translator.translate(text, src='sr', dest='ru')
    return result.text


def translate_to_sr(text):
    translator = Translator()
    result = translator.translate(text, src='ru', dest='sr')
    return result.text
