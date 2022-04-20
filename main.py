from fastapi import FastAPI
from schemas import Note


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/notes/")
async def all_notes():
    return {"message": f"All notes"}


@app.post("/notes/")
async def post_note(note: Note):
    return note


@app.get("/notes/{note_id}")
async def get_note_by_id(note_id: str):
    return {"message": f"Note id is {note_id}"}


@app.patch("/notes/{note_id}")
async def edit_note_by_id(note_id: str):
    return {"message": f"Note id is {note_id}"}
