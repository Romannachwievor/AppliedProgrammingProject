import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from exploration.main import app, get_session


@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)


def _valid_note(**overrides):
    """Return a valid NoteCreate payload, with optional field overrides."""
    data = {
        "title": "Valid Note Title",
        "content": "Some content here",
        "category": "work",
        "tags": ["work"],
    }
    data.update(overrides)
    return data


def test_create_note_rejects_short_title(client):
    """title shorter than 3 chars must return 422."""
    response = client.post("/notes", json=_valid_note(title="ab"))
    assert response.status_code == 422


def test_create_note_rejects_unknown_category(client):
    """category not in ALLOWED_CATEGORIES must return 422."""
    response = client.post("/notes", json=_valid_note(category="banana", tags=[]))
    assert response.status_code == 422


def test_create_note_normalizes_tags(client):
    """Tags are stripped, lowercased, and deduplicated before storing."""
    response = client.post(
        "/notes",
        json=_valid_note(tags=["URGENT", "urgent", "  meeting  ", "Q2", "work"]),
    )
    assert response.status_code == 201
    tags = response.json()["tags"]
    assert "urgent" in tags
    assert "meeting" in tags
    assert "q2" in tags
    assert tags.count("urgent") == 1  # deduped


def test_create_note_forbids_extra_fields(client):
    """Unknown fields must return 422 (extra='forbid')."""
    data = _valid_note()
    data["tagz"] = ["typo"]
    response = client.post("/notes", json=data)
    assert response.status_code == 422


def test_work_note_without_work_tag_is_allowed(client):
    """Day 6 suite expects work notes without an explicit 'work' tag to be valid."""
    response = client.post("/notes", json=_valid_note(category="work", tags=["meeting"]))
    assert response.status_code == 201


def test_patch_with_empty_body_succeeds(client):
    """PATCH with {} must succeed — no fields are changed."""
    create_resp = client.post("/notes", json=_valid_note())
    assert create_resp.status_code == 201
    note_id = create_resp.json()["id"]

    response = client.patch(f"/notes/{note_id}", json={})
    assert response.status_code == 200


def test_patch_with_invalid_title_fails(client):
    """PATCH with a title that is too short must return 422."""
    create_resp = client.post("/notes", json=_valid_note())
    assert create_resp.status_code == 201
    note_id = create_resp.json()["id"]

    response = client.patch(f"/notes/{note_id}", json={"title": ""})
    assert response.status_code == 422


def test_tag_name_rejects_uppercase(client):
    """Uppercase tags are normalized to lowercase, not stored as-is."""
    response = client.post(
        "/notes",
        json=_valid_note(tags=["UPPERCASE", "work"]),
    )
    assert response.status_code == 201
    tags = response.json()["tags"]
    assert "uppercase" in tags
    assert "UPPERCASE" not in tags
