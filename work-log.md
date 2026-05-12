# Work Log

**Roman Tonn:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?
- fast-api installiert
- main.py erstellt
- mit Funktion @app.get "Hello World!" und "Hello {name}!" getestet
- Funktion hinzugefügt, die eine gegebene Zahl dupliziert
- geändert zu Funktion, die die Zahl quadriert
- Presentation.md gecheckt - fand meinen code besser

---

#### 2. 🚧 What challenges did I face?
- Schreibweise für {"result": number ** 2} unklar





---

#### 3. 💡 How did I overcome them?
- schnelle Online-suche





---

### Day 2

#### 1. ✅ What did I accomplish?
- .gitignore gepusht
- marp installiert
- Folien in VS Code angeschaut
- main.py mit day-02-presentation verglichen
- Fehlende Notes-Endpunkte ergänzt (GET /notes/stats, GET /notes/{id})
- category bei NoteCreate und Note hinzugefügt
- FastAPI-Metadaten (title, description, version) korrekt an FastAPI() übergeben
- HTTPException für 404 bei GET /notes/{note_id} hinzugefügt




---

#### 2. 🚧 What challenges did I face?
- f-strings verstehen
- marp installieren (dachte es wäre ein Python package)
- Unterschiede zwischen main.py und Folien finden
- Reihenfolge bei den Note-Routen verstehen (/notes/stats muss vor /notes/{id} stehen)
- NoteCreate vs. Note Modelle falsch benannt (Groß-/Kleinschreibung)
- title/description/version waren standalone-Variablen, wurden nicht an FastAPI() übergeben




---

#### 3. 💡 How did I overcome them?
- Folien anschauen
- marp mit npm installiert
- Code Schritt für Schritt vergleichen
- Routen testen und Fehler prüfen
- Python-Konvention PascalCase nachgelesen (NoteCreate statt Notecreate)
- FastAPI-Doku geprüft: Metadaten gehören in FastAPI(...) nicht als separate Variablen




---

### Day 3

#### 1. ✅ What did I accomplish?
- REST-Designprinzipien gelernt (Ressourcen statt Verben, HTTP-Methoden, Status Codes)
- Path- vs. Query-Parameter verstanden
- main.py auf SQLite umgestellt (SQLModel statt JSON-Datei)
- tags-Feld zu NoteCreate und Note hinzugefügt (many-to-many via NoteTag-Tabelle)
- GET /notes mit Filtern erweitert: ?category=, ?search=, ?tag=
- PUT /notes/{id} für vollständiges Update implementiert
- PATCH /notes/{id} für partielles Update implementiert
- DELETE /notes/{id} implementiert
- GET /tags und GET /tags/{tag}/notes implementiert
- GET /categories und GET /categories/{category}/notes implementiert
- GET /notes/stats erweitert mit top_tags und unique_tags_count
- sqlmodel per uv add sqlmodel installiert


---

#### 2. 🚧 What challenges did I face?
- many-to-many-Beziehung zwischen Note und Tag verstehen
- Unterschied PUT vs. PATCH unklar
- Route /notes/stats muss vor /notes/{note_id} stehen (sonst wird "stats" als ID interpretiert)
- JSON-Storage durch Datenbanklogik ersetzen (Session, commit, refresh)


---

#### 3. 💡 How did I overcome them?
- Nils gefragt 👍





---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?
- test_day4.py und main_day4.py erstellt
- pytest, requests und Faker installiert
- Erster Test gegen laufenden Server ausgeführt: 1/1 passed
- test_day4.py erweitert (3/3 passed): test_greetings (Faker-Loop x10), test_is_adult (range 0–40, alle Felder geprüft), test_is_adult_negative_age
- Validierung für negative Altersangaben in main_day4.py ergänzt (400 Bad Request)
- test_notes.py erstellt: 17 Tests für Notes API (CRUD, Filter, Fehlerbehandlung, Day-3-Features)
- Pylance-Typfehler in main.py behoben (Problem in Workspace erkannt und von Copilot fixen lassen)

---

#### 2. 🚧 What challenges did I face?
- test_day4.py lief nicht
- requests-Modul fehlte
- Dateien waren nicht gespeichert (0 Bytes auf Festplatte)
- Server und Tests brauchen zwei separate Terminals
- Einrückungsfehler in test_is_adult
- test_is_adult_negative_age: main_day4.py validierte negative Zahlen nicht Test failte (Sinnvolle Ergänzung?)
- Pylance-Typfehler: str = None, Optional[int] -> int, Join mit col()



---

#### 3. 💡 How did I overcome them?
- Nicht gespeicherte .py mit Cmd+S gefixed
- uv add pytest && uv add requests && uv add Faker
- Falschen Text aus test_day4.py entfernt
- Server in Terminal 1, pytest in Terminal 2
- Einrückung korrigiert
- HTTPException(400) für negative Altersangaben in main_day4.py ergänzt
- Optional[str] statt str = None für Query-Parameter; col() für SQLModel-Joins; # type: ignore für __tablename__



---

### Day 5

#### 1. ✅ What did I accomplish?
- Strikte Schemas umgesetzt: `NoteCreate` und `NoteUpdate` mit Pydantic aufgebaut, inkl. Sperre für unbekannte Felder über `extra="forbid"`
- Feld Validierung und Normalisierung ergänzt: Längenregeln definiert sowie automatische Bereinigung mit strip/lowercase für category und tags
- Whitelist-Konzept angewendet: `ALLOWED_CATEGORIES` eingeführt und Kategorien darauf geprüft
- Cross Field Validierung umgesetzt: per `@model_validator(mode="after")` erzwungen, dass work Notizen auch das work Tag enthalten
- Tag Modell gehärtet: Name Validierung auf lowercase Buchstaben, Zahlen und Bindestrich sowie zusätzlicher Längenprüfung
- Pydantic v2 Standards angewendet: `ConfigDict` genutzt und `.dict()` auf `.model_dump()` umgestellt
- Validierung mit Tests abgesichert: `test_validation.py` mit 8 gezielten Tests (TestClient + In Memory SQLite, ohne laufenden Server)
- Bestehende API Tests kompatibel gemacht: `test_notes.py` auf gültige Kategorien aus `ALLOWED_CATEGORIES` angepasst


---

#### 2. 🚧 What challenges did I face?
- Validierungscode ohne Vorlesung verstehen (Arbeit ging vor)
- `sqlmodel.Field` akzeptiert Pydantic-Parameter wie `pattern` nicht -> `TypeError`
- Zwei Funktions-Bodies (`statement = select(Note)`, `notes = session.exec(...)`) beim Restore gelöscht
- `test_notes.py` vollständig rot: alte Testkategorien ("Testing", "FilterWork") jetzt ungültig


---

#### 3. 💡 How did I overcome them?
- Kommilitonen gefragt, Vorlesungsfolien nachgelesen
- `pydantic.Field as PydanticField` für BaseModels importiert, `sqlmodel.Field` für Tabellen-Modelle separat genutzt
- Fehler mit `get_errors`-Tool identifiziert, fehlende Zeilen manuell wiederhergestellt
- Alle Testkategorien konsistent auf `ALLOWED_CATEGORIES`-Werte umgestellt


---

### Day 6

#### 1. ✅ What did I accomplish?
- class_based_decorator.py umgesetzt (Class Decorator mit __call__, Logging und Laufzeitmessung)
- Referenz Test Suite aus Day 6 heruntergeladen
- Test Suite ausgeführt und Fehler analysiert
- main.py angepasst, damit die neue Suite läuft: Date Filter created_after und created_before ergänzt
- Top Tags in /notes/stats auf maximal 5 Einträge begrenzt
- Kompatibilitätsdatei main.py im Root ergänzt, damit Start mit main:app funktioniert
- Alle Day 6 Referenztests grün bekommen
- Lokale test_validation.py erneut geprüft und auf aktuellen Stand gebracht
- Serverabhängige Tests robuster gemacht: test_notes.py und test_day4.py skippen, wenn kein passender Server läuft

---

#### 2. 🚧 What challenges did I face?
- Neue externe Test Suite hatte andere Erwartungen als Day 5 Regeln
- Viele Failures durch zu strikte work Tag Regel
- Date Filter Parameter fehlten komplett in GET /notes
- pytest -q lokal fehlerhaft, wenn kein Server läuft
- Unterschied zwischen Day 4 Demo API und aktueller Notes API führte zu instabilen Requests Tests

---

#### 3. 💡 How did I overcome them?
- Fehlerausgabe aus pytest Schritt für Schritt gelesen und nach Ursachen gruppiert
- API Verhalten an Referenzsuite angepasst (work Tag Regel gelockert, Date Filter ergänzt)
- Endpoints mit erneutem Testlauf validiert bis 70 von 70 Tests bestanden
- test_validation separat gegen In Memory SQLite geprüft, damit frühere Day 5 Funktionen nicht kaputtgehen
- Automatische Skip Regeln in serverabhängigen Testdateien eingebaut, damit Tests ohne laufenden Server nicht fehlschlagen

---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?
- Streamlit als Frontend Tool eingerichtet und erste App erstellt
- No API Test Teil umgesetzt (Button sendet Request an no as a service und zeigt Antwort)
- frontend.py für Notes API erstellt
- Funktion 1 umgesetzt: Alle Notes laden und Titel in Liste anzeigen
- Detailansicht für ausgewählte Note ergänzt (Titel, Inhalt, Kategorie, Tags)
- Funktion 2 umgesetzt: Neue Note über Formular anlegen (Titel, Inhalt, Kategorie, Tags)
- Nach dem Erstellen erneut geladen, damit neue Notes direkt in der Liste erscheinen
- Session State Anzeige über Expander ergänzt

---

#### 2. 🚧 What challenges did I face?
- Streamlit war anfangs nicht in der aktiven Umgebung verfügbar
- Fehlerbehandlung für API Requests in der UI fehlte zuerst
- Tags Eingabe aus Textfeld musste sauber in Liste umgewandelt werden


---

#### 3. 💡 How did I overcome them?
- streamlit direkt in die aktive .venv installiert
- Requests mit try/except abgesichert und Fehlermeldungen im UI angezeigt
- Hilfsfunktion für Tag Parsing eingebaut (Komma getrennte Eingabe -> Liste)
- Frontend mit laufender FastAPI getestet und Formular mit st.form umgesetzt

---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













