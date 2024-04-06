# import ngrok python sdk
import ngrok
import config
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    
    listener = ngrok.forward(8000, authtoken_from_env=True)
    print(f"Ingress established at {listener.url()}")
    
    with open("shared/forward_url.txt", "w") as f:
        f.write(listener.url())

    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    