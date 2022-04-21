import uvicorn
from fastapi import FastAPI
from app.config import get_config
from app.database import db
from app.api import notes

app = FastAPI()

app.include_router(notes.router, prefix="/api/notes")


@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(path=config.db_path, name=config.db_name)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
