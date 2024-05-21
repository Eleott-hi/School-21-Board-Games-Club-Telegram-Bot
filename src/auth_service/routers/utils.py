from fastapi import HTTPException, Request, status


def get_telegram_id(request: Request):
    id = request.headers.get("X-Telegram-ID")

    print("Telegram ID:", id)

    if id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Auth Header "X-Telegram-ID"',
        )

    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Auth Header "X-Telegram-ID"',
        )

    return id
