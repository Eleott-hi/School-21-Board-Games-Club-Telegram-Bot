from fastapi import FastAPI

from database.database import init_db
from contextlib import asynccontextmanager
from routers.BookingRouter import router as booking_router
from routers.RoomRouter import router as room_router
from routers.UserRouter import router as user_router
from routers.ViolationRouter import router as violation_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Booking REST API",
    description="Service to manage room booking",
    version="1.0.0",
    root_path="/booking_service",
)

app.include_router(booking_router)
app.include_router(room_router)
app.include_router(user_router)
app.include_router(violation_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )