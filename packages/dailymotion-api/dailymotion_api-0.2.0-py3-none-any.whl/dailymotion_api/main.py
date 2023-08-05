import uvicorn

from fastapi import FastAPI

from routes.routes import router


app = FastAPI(
    title="dailymotion_api",
    description=(
        "This is an API developed un python, using FastAPI."
        "In wich, you can see 10 different videos about gaming."
    )
)

app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )