# AppliedProgrammingProject

Notes-Management-Projekt aus dem Applied-Programming-Kurs mit:

- FastAPI-Backend (CRUD, Filter, Stats, Kategorien, Tags)
- SQLModel + SQLite Persistenz
- Streamlit-Frontend für API-Interaktion

## Projektstruktur

- `exploration/main.py`: Hauptimplementierung der FastAPI-Anwendung
- `main.py`: Kompatibler Einstiegspunkt
- `frontend.py`: Streamlit-Frontend
- `notes.db`: SQLite-Datenbank
- `test_*.py`: Test-Suiten

## Voraussetzungen

- Python 3.14+
- `uv` installiert (empfohlen)

## Installation

```bash
git clone https://github.com/Romannachwievor/AppliedProgrammingProject.git
cd AppliedProgrammingProject/AppliedProgrammingProject
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

Alternative mit venv + pip:

```bash
git clone https://github.com/Romannachwievor/AppliedProgrammingProject.git
cd AppliedProgrammingProject/AppliedProgrammingProject
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Anwendung starten

1. Backend starten (FastAPI)

```bash
uv run fastapi dev main.py
```

Backend laeuft dann unter:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

2. Frontend starten (Streamlit)

```bash
uv run streamlit run frontend.py --server.port 8501
```

Frontend erreichbar unter:

- http://localhost:8501

## API-Beispiele

### Notiz anlegen (POST /notes)

```python
import requests

payload = {
	"title": "Sprint Planning",
	"content": "Backlog fuer naechste Woche priorisieren",
	"category": "work",
	"tags": ["planning", "team"],
}

res = requests.post("http://127.0.0.1:8000/notes", json=payload, timeout=10)
res.raise_for_status()
print(res.json())
```

### Notizen abholen (GET /notes)

```python
import requests

res = requests.get("http://127.0.0.1:8000/notes", timeout=10)
res.raise_for_status()

for note in res.json():
	print(note["id"], note["title"], note["category"], note["tags"])
```

Mit Filtern:

```python
import requests

res = requests.get(
	"http://127.0.0.1:8000/notes",
	params={"category": "work", "tag": "urgent", "search": "meeting"},
	timeout=10,
)
res.raise_for_status()
print(res.json())
```

## Tests ausfuehren

```bash
uv run pytest -q
```

Hinweis: Einige Integrationstests erwarten einen laufenden Server auf `127.0.0.1:8000`.
