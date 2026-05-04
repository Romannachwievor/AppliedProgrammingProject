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
fast-api installiert
main.py erstellt
mit Funktion @app.get "Hello World!" und "Hello {name}!" getestet 
Funktion hinzugefügt, die eine gegebene Zahl dupliziert
    geändert zu Funktion, die die Zahl quadriert
Presentation.md gecheckt - fand meinen code besser

---

#### 2. 🚧 What challenges did I face?
Schreibweise für {"result": number ** 2} unklar





---

#### 3. 💡 How did I overcome them?
schnelle Online-suche





---

### Day 2

#### 1. ✅ What did I accomplish?
.gitignore gepusht
marp installiert
Folien in VS Code angeschaut
main.py mit day-02-presentation verglichen
Fehlende Notes-Endpunkte ergänzt (GET /notes/stats, GET /notes/{id})
category bei NoteCreate und Note hinzugefügt
FastAPI-Metadaten (title, description, version) korrekt an FastAPI() übergeben
HTTPException für 404 bei GET /notes/{note_id} hinzugefügt




---

#### 2. 🚧 What challenges did I face?
f-strings verstehen
marp installieren (dachte es wäre ein Python package)
Unterschiede zwischen main.py und Folien finden
Reihenfolge bei den Note-Routen verstehen (/notes/stats muss vor /notes/{id} stehen)
NoteCreate vs. Note Modelle falsch benannt (Groß-/Kleinschreibung)
title/description/version waren standalone-Variablen, wurden nicht an FastAPI() übergeben




---

#### 3. 💡 How did I overcome them?
Folien anschauen
marp mit npm installiert
Code Schritt für Schritt vergleichen
Routen testen und Fehler prüfen
Python-Konvention PascalCase nachgelesen (NoteCreate statt Notecreate)
FastAPI-Doku geprüft: Metadaten gehören in FastAPI(...) nicht als separate Variablen




---

### Day 3

#### 1. ✅ What did I accomplish?
REST-Designprinzipien gelernt (Ressourcen statt Verben, HTTP-Methoden, Status Codes)
Path- vs. Query-Parameter verstanden
main.py auf SQLite umgestellt (SQLModel statt JSON-Datei)
tags-Feld zu NoteCreate und Note hinzugefügt (many-to-many via NoteTag-Tabelle)
GET /notes mit Filtern erweitert: ?category=, ?search=, ?tag=
PUT /notes/{id} für vollständiges Update implementiert
PATCH /notes/{id} für partielles Update implementiert
DELETE /notes/{id} implementiert
GET /tags und GET /tags/{tag}/notes implementiert
GET /categories und GET /categories/{category}/notes implementiert
GET /notes/stats erweitert mit top_tags und unique_tags_count
sqlmodel per uv add sqlmodel installiert


---

#### 2. 🚧 What challenges did I face?
many-to-many-Beziehung zwischen Note und Tag verstehen
Unterschied PUT vs. PATCH unklar
Route /notes/stats muss vor /notes/{note_id} stehen (sonst wird "stats" als ID interpretiert)
JSON-Storage durch Datenbanklogik ersetzen (Session, commit, refresh)


---

#### 3. 💡 How did I overcome them?






---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?
test_day4.py und main_day4.py erstellt
pytest und requests installiert
Test gegen laufenden Server ausgeführt 1/1 passed
test_day4.py erweitert: 3/3 passed
faker importiert

---

#### 2. 🚧 What challenges did I face?
test_day4.py lief nicht
requests-Modul fehlte
Dateien waren nicht gespeichert (0 Bytes auf Festplatte)
Server und Tests brauchen zwei separate Terminals



---

#### 3. 💡 How did I overcome them?
Nicht gespeicherte .py, mit Cmd+S gefixed
uv add pytest && uv add requests
falschen Text aus test_day4.py entfernt
Server in Terminal 1, pytest in Terminal 2



---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






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













