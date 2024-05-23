from enum import Enum
import json
from typing import Any, Dict


class Language(str, Enum):
    RU = "ru"
    EN = "en"


class WordMap:
    def __init__(self, word_map: Dict[str, str] | None = None) -> None:
        self.word_map = word_map if word_map else {}

    def __getitem__(self, key) -> str:
        if key in self.word_map:
            return self.word_map[key]

        return "[not implemented]"


class Localization:
    def __init__(self, language: Language = Language.RU) -> None:
        self.language = language
        self.parse_text()

    def set_language(self, language: Language):
        self.language = language
        self.parse_text()

    def parse_text(self):
        file = f"resources/text/{self.language.value}.json"

        with open(file, encoding="utf-8") as f:
            texts: Dict[str, Any] = json.load(f)

        self.texts = {}

        for window, words_map in texts.items():
            self.texts[window] = WordMap(words_map)

    def __getitem__(self, window) -> Dict[str, Any]:
        return self.texts.get(window, WordMap())


class LocalizationManager:
    def __init__(self) -> None:
        self.localizations = {
            Language.RU: Localization(Language.RU),
            Language.EN: Localization(Language.EN),
        }

    def __getitem__(self, item: str | Language) -> Localization:
        item = Language(item)

        return self.localizations.get(item)


localization = Localization(Language.RU)

localization_manager = LocalizationManager()
