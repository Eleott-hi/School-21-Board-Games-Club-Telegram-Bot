import random
from fastapi import APIRouter, Body, Depends, HTTPException
from schemas.auth_schemas import ConfirmSchema, RegisterSchema, User
from services.auth_service import AuthService
from repositories.auth_repository import AuthRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"description": "Not authorized"}},
)


@router.post("/register")
async def register(
    register_schema: RegisterSchema,
    auth_service: AuthService = Depends(),
):
    print(register_schema)
    await auth_service.start_registeration(register_schema)


@router.post("/confirm_token")
async def confirm_token(
    confirm_schema: ConfirmSchema,
    auth_service: AuthService = Depends(),
):
    await auth_service.confirm_token(confirm_schema)


@router.get("/user/{telegram_id}")
async def get_user(
    telegram_id: int,
    auth_service: AuthService = Depends(),
) -> User:
    return await auth_service.get_user_by_telegram_id(telegram_id)


# @router.get("/test", tags=["test"])
# async def root():
#     return "Hello, from auth!"


# @router.post("/register", tags=["auth", "register"])
# async def register():
#     return


# @router.post("/login", tags=["auth", "login"])
# async def login():
#     return


# @router.post("/logout", tags=["auth", "logout"])
# async def logout():
#     return


# @router.post("/refresh", tags=["auth", "refresh"])
# async def refresh():
#     return


# @router.post("/forgot-password", tags=["auth", "forgot-password"])
# async def forgot_password():
#     return

# @router.post("/change-password", tags=["auth", "change-password"])
# async def change_password():
#     return

# @router.get(
#     "/user",
#     tags=["auth", "user"],
#     responses={401: {"description": "Not authorized"}},
# )
# async def get_user():
#     if random.choice([True, False]):
#         raise HTTPException(status_code=401, detail="Not authorized")

#     return dict(name="some name")
