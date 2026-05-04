import requests

BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def create_test_note(
    title="Test Note",
    content="Test content",
    category="Testing",
    tags=None,
):
    """Create a note and return the response JSON. Asserts 201."""
    if tags is None:
        tags = ["test", "pytest"]
    response = requests.post(
        f"{BASE_URL}/notes",
        json={"title": title, "content": content, "category": category, "tags": tags},
    )
    assert response.status_code == 201
    return response.json()


# ---------------------------------------------------------------------------
# CRUD Tests
# ---------------------------------------------------------------------------

def test_create_note():
    """Test creating a new note returns 201 with correct fields."""
    data = create_test_note(title="My Note", category="Work", tags=["important"])

    assert "id" in data
    assert "created_at" in data
    assert data["title"] == "My Note"
    assert data["category"] == "Work"
    assert "important" in data["tags"]


def test_list_notes():
    """Test GET /notes returns a list."""
    response = requests.get(f"{BASE_URL}/notes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_note_by_id():
    """Test GET /notes/{id} returns the correct note."""
    created = create_test_note(title="Get By ID Note")
    note_id = created["id"]

    response = requests.get(f"{BASE_URL}/notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Get By ID Note"


def test_update_note():
    """Test PUT /notes/{id} replaces all fields."""
    created = create_test_note(title="Original Title")
    note_id = created["id"]

    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": "Updated",
        "tags": ["updated"],
    }
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["category"] == "Updated"
    assert "updated" in data["tags"]


def test_delete_note():
    """Test DELETE /notes/{id} removes the note."""
    created = create_test_note(title="To Be Deleted")
    note_id = created["id"]

    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code == 204

    # Verify it is gone
    get_response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert get_response.status_code == 404


# ---------------------------------------------------------------------------
# Filtering Tests
# ---------------------------------------------------------------------------

def test_filter_by_category():
    """Test ?category= returns only notes with that category."""
    create_test_note(title="Work Note 1", category="FilterWork", tags=[])
    create_test_note(title="Work Note 2", category="FilterWork", tags=[])

    response = requests.get(f"{BASE_URL}/notes?category=FilterWork")

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 2
    for note in notes:
        assert note["category"] == "FilterWork"


def test_filter_by_search():
    """Test ?search= returns notes containing the search term."""
    create_test_note(
        title="Unique Search Term XYZ123",
        content="Some content",
        category="Search",
        tags=[],
    )

    response = requests.get(f"{BASE_URL}/notes?search=XYZ123")

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 1
    for note in notes:
        text = note["title"].lower() + note["content"].lower()
        assert "xyz123" in text


def test_filter_by_tag():
    """Test ?tag= returns only notes with that tag."""
    create_test_note(title="Tagged Note", category="Tagging", tags=["uniquetag999"])

    response = requests.get(f"{BASE_URL}/notes?tag=uniquetag999")

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 1
    for note in notes:
        assert "uniquetag999" in note["tags"]


def test_combined_filters():
    """Test combining category + tag filters together."""
    create_test_note(
        title="Combined Filter Note",
        category="CombinedCat",
        tags=["combinedtag"],
    )

    response = requests.get(
        f"{BASE_URL}/notes?category=CombinedCat&tag=combinedtag"
    )

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 1
    for note in notes:
        assert note["category"] == "CombinedCat"
        assert "combinedtag" in note["tags"]


# ---------------------------------------------------------------------------
# Error Case Tests
# ---------------------------------------------------------------------------

def test_create_note_missing_field():
    """Test creating a note with missing required fields returns 422."""
    response = requests.post(
        f"{BASE_URL}/notes",
        json={"title": "Only Title"},  # missing content and category
    )

    assert response.status_code == 422


def test_get_nonexistent_note():
    """Test GET /notes/99999 returns 404."""
    response = requests.get(f"{BASE_URL}/notes/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_note():
    """Test PUT /notes/99999 returns 404."""
    response = requests.put(
        f"{BASE_URL}/notes/99999",
        json={"title": "X", "content": "X", "category": "X", "tags": []},
    )

    assert response.status_code == 404


def test_delete_nonexistent_note():
    """Test DELETE /notes/99999 returns 404."""
    response = requests.delete(f"{BASE_URL}/notes/99999")

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Day 3 Feature Tests
# ---------------------------------------------------------------------------

def test_notes_statistics():
    """Test GET /notes/stats returns expected fields."""
    create_test_note(title="Stats Note", category="StatsCategory", tags=["statstag"])

    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_notes" in data
    assert "by_category" in data
    assert "top_tags" in data
    assert isinstance(data["total_notes"], int)
    assert data["total_notes"] >= 1


def test_patch_note_title_only():
    """Test PATCH /notes/{id} updates only the title, leaves other fields intact."""
    created = create_test_note(
        title="Original", content="Keep this", category="KeepCat", tags=["keeptag"]
    )
    note_id = created["id"]

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}", json={"title": "Patched Title"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Patched Title"
    assert data["content"] == "Keep this"
    assert data["category"] == "KeepCat"
    assert "keeptag" in data["tags"]


def test_list_categories():
    """Test GET /categories returns a sorted list of strings."""
    create_test_note(title="Cat Note", category="CategoryEndpointTest", tags=[])

    response = requests.get(f"{BASE_URL}/categories")

    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert "CategoryEndpointTest" in categories


def test_notes_by_category_endpoint():
    """Test GET /categories/{category}/notes returns only matching notes."""
    create_test_note(title="CatRoute Note", category="CatRouteTest", tags=[])

    response = requests.get(f"{BASE_URL}/categories/CatRouteTest/notes")

    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 1
    for note in notes:
        assert note["category"] == "CatRouteTest"
