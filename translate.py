from googletrans import Translator


def translator(text, language_code):
    trans = Translator()
    translated = trans.translate(text, dest=language_code)
    return translated.text
