from enum import Enum
import json


class Language(str, Enum):
    RU = "ru"
    EN = "en"


class LocalizationManager:
    def __init__(self, language: Language = Language.RU) -> None:
        self.language = language
        self.parse_text()

    def set_language(self, language: Language):
        self.language = language
        self.parse_text()

    def parse_text(self):
        file = f"resources/text/{self.language.value}.json"
        with open(file, encoding="utf-8") as f:
            self.texts = json.load(f)

    def __getitem__(self, item):
        return self.texts.get(item)


localization = LocalizationManager(Language.RU)
