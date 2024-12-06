from translate import Translator

class Translator:
    def __init__(self):
        # Set up a translator with a default language (for example, Spanish)
        self.default_lang = "es"

    def translate(self, text, target_language=None):
        """Translates the text to the target language (defaults to Spanish)."""
        if target_language is None:
            target_language = self.default_lang
        translator = Translator(to_lang=target_language)
        return translator.translate(text)
