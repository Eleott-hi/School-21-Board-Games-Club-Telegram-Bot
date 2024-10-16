import config.config
import config.logger

from fastapi import Depends, FastAPI
from routers.booking_router import router as booking_router
from database.database import init_db


async def lifespan(app):
    await init_db()
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="Booking Service",
    description="Service to manage game bookings",
    version="0.0.1",
    root_path="/api/v1",
)


app.include_router(booking_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
