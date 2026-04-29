from fastapi import FastAPI

from src.routers import router

app = FastAPI(title="JWT Auth Lesson")


app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def start():
    import uvicorn

    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()
