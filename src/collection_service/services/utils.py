import json
import httpx
from fastapi import HTTPException


def get_fastapi_error(response: httpx.Response) -> HTTPException:
    err = json.loads(response.text)

    return HTTPException(
        status_code=response.status_code,
        detail=err["detail"],
    )
