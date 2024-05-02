from typing import List, Dict
from database.database import games
from services.utils import async_wait


class GameService:
    @classmethod
    @async_wait()
    async def get_games(cls, filters: Dict):
        print(filters, flush=True)
        offset = filters.get("offset", 0)
        limit = filters.get("limit", 3)
        title = filters.get("title", None)

        res = games
        if title:
            res = await cls.get_games_by_str_in_title(title)

        total = len(res)
        from_ = offset
        to_ = from_ + limit
        has_prev = offset > 0
        has_next = to_ < total

        return dict(
            games=res[from_:to_],
            total=total,
        )

    @classmethod
    @async_wait()
    async def get_game_by_id(cls, id: str) -> Dict:
        return list(filter(lambda x: x["id"] == id, games))[0]

    @classmethod
    @async_wait()
    async def get_games_by_str_in_title(cls, title: str) -> List[Dict]:
        title = title.strip().lower()
        return list(filter(lambda x: title in x["title"].lower(), games))
