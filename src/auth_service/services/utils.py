import json


def get_fastapi_error_detail(response: str):
    res = json.loads(response)

    if "detail" in res:
        return res["detail"]

    return response
