# from datetime import datetime, timedelta
# from typing import List
# from uuid import UUID
# from routers.schemas import UserInfo
# from fastapi import Depends, Request, HTTPException, status
# import httpx
# from postgres_service.config import AUTH_SERVICE
# import requests


# def get_user(request: Request) -> UserInfo:
#     url = f"http://{AUTH_SERVICE}/auth/user"
#     headers = dict(request.headers)

#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=response.status_code,
#             detail=response.text,
#         )

#     user = response.json()
#     print("RESPONSE:", user)
#     user = UserInfo(**user)

#     return user


# async def get_admin(user: UserInfo = Depends(get_user)) -> UserInfo:
#     if user.role != Role.ADMIN:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="No administrator rights",
#         )

#     return user
