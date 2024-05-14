from fastapi import FastAPI
from routers.mail_router import router as mail_router

app: FastAPI = FastAPI(
    title="Mail Service",
    description="Service to manage mailing",
    version="0.0.1",
    root_path="/api/v1",
)

app.include_router(mail_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
