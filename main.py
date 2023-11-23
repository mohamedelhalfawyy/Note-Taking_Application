# app/api/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.crud import create_note, read_note, update_note, delete_note, read_notes
from database.connection import get_db
from api.models import NoteCreate, NoteUpdate, NoteResponse
from utils.openai_utils import get_openai_api_key, summarize_note

app = FastAPI(
    title="Notes Server",
    version="1.0",
    description="A simple api server for Note-Taking Application"
)

@app.post("/notes/", response_model=NoteResponse)
async def create_note_route(note: NoteCreate, db: Session = Depends(get_db)):
    return create_note(db, note)

@app.get("/notes/{note_id}", response_model=NoteResponse)
def read_note_route(note_id: int, db: Session = Depends(get_db)):
    return read_note(db, note_id)

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note_route(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    return update_note(db, note_id, note)

@app.delete("/notes/{note_id}", response_model=NoteResponse)
def delete_note_route(note_id: int, db: Session = Depends(get_db)):
    return delete_note(db, note_id)

@app.get("/notes/", response_model=list[NoteResponse])
def read_notes_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return read_notes(db, skip, limit)

@app.get("/summarize/")
def summarize_note_route(note_id: int, openai_api_key: str = Depends(get_openai_api_key) ,db: Session = Depends(get_db)):
    return summarize_note(db, note_id, openai_api_key)