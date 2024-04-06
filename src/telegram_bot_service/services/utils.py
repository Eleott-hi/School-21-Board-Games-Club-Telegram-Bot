from typing import List, Dict

from database.database import games


def filter_by_title(title: str) -> List[Dict]:
    title = title.strip().lower()

    return list(
        filter(
            lambda x: title in x["gameName"].lower(),
            games
        )
    )


def get_game_by_id(id: str) -> Dict:
    return list(filter(lambda x: x["id"] == id, games))[0]


def get_all_games():
    return games


