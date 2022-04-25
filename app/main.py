import uvicorn
from fastapi import FastAPI

from app.config import get_config
from app.database import db
from app.api import notes, templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
config = get_config()

app.include_router(notes.router, prefix="/notes")
app.include_router(templates.router, prefix="/templates")

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
    await db.connect_to_database(path=config.db_path, name=config.db_name)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
