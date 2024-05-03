from db.database import get_session, AsyncSession, select
from db.models import BoardGame
from routers.schemas import Filters

def filters_to_boardgame(filters: Filters) -> BoardGame:
    filter_values = {k: v for k, v in filters.dict().items() if v is not None}
    board_game = BoardGame(**filter_values)
    
    return board_game


async def get_id_by_name(name):
    session: AsyncSession = get_session()
    stmt = select(BoardGame).where(BoardGame.gameName == name)
    result = await session.exec(stmt)
    result_data = [obj.id for obj in result.all()]
    return result_data

async def change_state(data):
    session: AsyncSession = get_session()
    stmt = select(BoardGame).where(BoardGame.gameName == data.gameName)
    result = await session.exec(stmt)
    result_data = result.all()
    if result_data:
        for game in result_data:
            game.status = data.status
            await session.commit()
        return True
    else:
        return False