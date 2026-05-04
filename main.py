from datetime import datetime
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, or_, select
from sqlalchemy import and_


# ============================================================================
# DATABASE MODELS
# ============================================================================

class NoteTag(SQLModel, table=True):
    """Association table for the many-to-many relationship between Note and Tag."""
    __tablename__ = "note_tag"  # type: ignore[assignment]

    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)


class Note(SQLModel, table=True):
    __tablename__ = "notes"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.now)

    tags: list["Tag"] = Relationship(back_populates="notes", link_model=NoteTag)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    notes: list[Note] = Relationship(back_populates="tags", link_model=NoteTag)


# ============================================================================
# DATABASE SETUP
# ============================================================================

engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# ============================================================================
# PYDANTIC MODELS (API input / output)
# ============================================================================

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str

    class Config:
        from_attributes = True


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None


# ============================================================================
# HELPER
# ============================================================================

def get_or_create_tags(tag_names: list[str], session: Session) -> list[Tag]:
    """Normalize tag names and return Tag objects, creating new ones as needed."""
    tag_objects: list[Tag] = []
    seen: set[str] = set()

    for raw_name in tag_names:
        name = raw_name.lower().strip()
        if not name or name in seen:
            continue
        seen.add(name)

        existing = session.exec(select(Tag).where(Tag.name == name)).first()
        if existing:
            tag_objects.append(existing)
        else:
            new_tag = Tag(name=name)
            session.add(new_tag)
            tag_objects.append(new_tag)

    return tag_objects


def note_to_response(note: Note) -> NoteResponse:
    return NoteResponse(
        id=note.id or 0,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at.isoformat(),
    )


# ============================================================================
# APP
# ============================================================================

app = FastAPI(
    title="Applied Programming Course HS Coburg",
    description="Note Management API",
    version="1.0.0",
)


# ============================================================================
# BASIC ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello {name}!"}


@app.get("/square/{number}")
def calculate_square(number: int):
    result = number * number
    return {
        "number": number,
        "square": result,
        "calculation": f"{number} × {number} = {result}",
    }


@app.get("/double/{number}")
def calculate_double(number: int):
    result = number * 2
    return {
        "number": number,
        "double": result,
        "calculation": f"{number} × 2 = {result}",
    }


@app.get("/student")
def get_student():
    return {
        "name": "Roman Tonn",
        "semester": 1,
        "course": "Wirtschaftsinformatik 2.0",
        "university": "HS Coburg",
    }


# ============================================================================
# NOTES ENDPOINTS
# ============================================================================

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note."""
    db_note = Note(title=note.title, content=note.content, category=note.category)
    db_note.tags = get_or_create_tags(note.tags, session)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return note_to_response(db_note)


@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None,
) -> list[NoteResponse]:
    """List notes with optional filters (category, search text, tag)."""
    statement = select(Note)

    if category:
        statement = statement.where(Note.category == category)

    if search:
        search_lower = search.lower()
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search_lower}%"),
                col(Note.content).ilike(f"%{search_lower}%"),
            )
        )

    if tag:
        tag_lower = tag.lower()
        statement = (
            statement
            .join(NoteTag, col(NoteTag.note_id) == col(Note.id))  # type: ignore[arg-type]
            .join(Tag, col(Tag.id) == col(NoteTag.tag_id))  # type: ignore[arg-type]
            .where(col(Tag.name) == tag_lower)
        )

    notes = session.exec(statement).all()
    return [note_to_response(n) for n in notes]


@app.get("/notes/stats")
def get_notes_stats(session: SessionDep):
    """Get aggregated statistics: total, by category, top tags."""
    notes = session.exec(select(Note)).all()

    categories: dict[str, int] = {}
    tag_counts: dict[str, int] = {}

    for note in notes:
        categories[note.category] = categories.get(note.category, 0) + 1
        for tag in note.tags:
            tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

    top_tags = [
        {"tag": name, "count": count}
        for name, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "total_notes": len(notes),
        "by_category": categories,
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counts),
    }


@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> NoteResponse:
    """Get a specific note by ID."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    return note_to_response(note)


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> NoteResponse:
    """Replace all fields of an existing note (full update)."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    note.tags = get_or_create_tags(note_update.tags, session)

    session.commit()
    session.refresh(note)
    return note_to_response(note)


@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate, session: SessionDep) -> NoteResponse:
    """Update only the provided fields of a note (partial update)."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

    update_data = note_update.dict(exclude_unset=True)

    if "tags" in update_data:
        note.tags = get_or_create_tags(update_data.pop("tags"), session)

    for key, value in update_data.items():
        setattr(note, key, value)

    session.add(note)
    session.commit()
    session.refresh(note)
    return note_to_response(note)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Delete a note."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    session.delete(note)
    session.commit()


# ============================================================================
# TAGS ENDPOINTS (Day 3)
# ============================================================================

@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    """Get all unique tags (sorted alphabetically)."""
    tags = session.exec(select(Tag)).all()
    return sorted(tag.name for tag in tags)


@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes that have a specific tag."""
    tag = session.exec(select(Tag).where(Tag.name == tag_name.lower())).first()
    if not tag:
        return []
    return [note_to_response(note) for note in tag.notes]


# ============================================================================
# CATEGORIES ENDPOINTS (Day 3)
# ============================================================================

@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    """Get all unique categories (sorted alphabetically)."""
    categories = session.exec(select(Note.category).distinct()).all()
    return sorted(categories)


@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes in a specific category."""
    notes = session.exec(select(Note).where(Note.category == category_name)).all()
    return [note_to_response(note) for note in notes]