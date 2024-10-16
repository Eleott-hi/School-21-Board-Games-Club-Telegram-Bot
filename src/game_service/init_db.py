import pandas as pd
import logging
import os
import asyncio

from models.Game import Base as booking_base
from database.database import engine, async_session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(booking_base.metadata.create_all)

    df = pd.read_csv("data/games.tsv", sep="\t")
    df["title"] = df["russian_name"] + df["english_name"].apply(
        lambda x: f" ({x})" if x else ""
    )
    df["complexity"] = pd.cut(
        df["complexity"].str.replace(",", ".").astype(float),
        bins=[-float("inf"), 2, 3, 4, float("inf")],
        labels=["easy", "medium", "hard", "hardcore"],
    )
    df["genres"] = df["genres"].str.split(",")

    async with async_session() as session:
        from repositories.games_repository import GamesRepository
        from schemas.schemas import GameRequest

        repository = GamesRepository(session)
        for _, game in df.iterrows():
            game = {k: (None if pd.isna(v) else v) for k, v in game.to_dict().items()}
            print(game, flush=True)
            await repository.create(GameRequest.model_validate(game, strict=False))


if __name__ == "__main__":

    asyncio.run(init_db())
