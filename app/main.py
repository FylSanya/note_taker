import uvicorn
from fastapi import FastAPI
from app.config import get_config
from app.database import db
from app.api import notes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(notes.router, prefix="/api/notes")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(path=config.db_path, name=config.db_name)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
