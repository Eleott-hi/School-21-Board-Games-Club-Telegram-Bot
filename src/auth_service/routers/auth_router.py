import random
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"description": "Not authorized"}},
)


@router.get("/test", tags=["test"])
async def root():
    return "Hello, from auth!"


@router.post("/register", tags=["auth", "register"])
async def register():
    return


@router.post("/login", tags=["auth", "login"])
async def login():
    return


@router.post("/logout", tags=["auth", "logout"])
async def logout():
    return


@router.post("/refresh", tags=["auth", "refresh"])
async def refresh():
    return


@router.post("/forgot-password", tags=["auth", "forgot-password"])
async def forgot_password():
    return

@router.post("/change-password", tags=["auth", "change-password"])
async def change_password():
    return

@router.get(
    "/user",
    tags=["auth", "user"],
    responses={401: {"description": "Not authorized"}},
)
async def get_user():
    if random.choice([True, False]):
        raise HTTPException(status_code=401, detail="Not authorized")

    return dict(name="some name")


