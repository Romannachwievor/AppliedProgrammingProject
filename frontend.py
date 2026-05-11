import requests
import streamlit as st

NO_API_URL = "https://naas.isalman.dev/no"
DEFAULT_NOTES_API_BASE_URL = "http://127.0.0.1:8000"
ALLOWED_CATEGORIES = ["work", "personal", "school", "ideas", "general"]


def request_no() -> str:
    response = requests.get(NO_API_URL, timeout=10)
    response.raise_for_status()
    return response.json()["reason"]


def fetch_notes(base_url: str) -> list[dict]:
    response = requests.get(f"{base_url}/notes", timeout=10)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, list) else []


def create_note(base_url: str, title: str, content: str, category: str, tags: list[str]) -> None:
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
    }
    response = requests.post(f"{base_url}/notes", json=payload, timeout=10)
    response.raise_for_status()


def parse_tags(tags_input: str) -> list[str]:
    if not tags_input.strip():
        return []
    return [tag.strip() for tag in tags_input.split(",") if tag.strip()]


def render_no_demo() -> None:
    st.subheader("Teil A: Say No Test App")

    if "no_text" not in st.session_state:
        st.session_state["no_text"] = ""

    if st.button("Neues No laden", use_container_width=True):
        try:
            st.session_state["no_text"] = request_no()
        except requests.RequestException as exc:
            st.session_state["no_text"] = f"Fehler beim Laden: {exc}"

    if not st.session_state["no_text"]:
        st.caption("Klicke auf den Button, um einen Text von der API zu laden.")
    else:
        st.info(st.session_state["no_text"])


def render_create_note_form(base_url: str) -> None:
    st.subheader("Neue Note erstellen")

    with st.form("create_note_form", clear_on_submit=False):
        title = st.text_input("Titel", placeholder="z. B. Sprint Planning")
        content = st.text_area("Inhalt", placeholder="Notizinhalt eingeben...")
        category = st.selectbox("Kategorie", options=ALLOWED_CATEGORIES)
        tags_input = st.text_input(
            "Tags (Komma getrennt)",
            placeholder="api, kurs, wichtig",
        )
        submit = st.form_submit_button("Note erstellen", use_container_width=True)

    if not submit:
        return

    if not title.strip() or not content.strip():
        st.warning("Titel und Inhalt sind Pflichtfelder.")
        return

    tags = parse_tags(tags_input)
    try:
        create_note(
            base_url=base_url,
            title=title,
            content=content,
            category=category,
            tags=tags,
        )
        st.success("Note erfolgreich erstellt")
    except requests.HTTPError as exc:
        if exc.response is not None:
            st.error(f"API Fehler {exc.response.status_code}: {exc.response.text}")
        else:
            st.error(f"API Fehler: {exc}")
    except requests.RequestException as exc:
        st.error(f"Backend nicht erreichbar: {exc}")


def render_notes_list(base_url: str) -> None:
    st.subheader("Alle Notes")

    if st.button("Liste aktualisieren", use_container_width=True):
        st.rerun()

    try:
        notes = fetch_notes(base_url)
    except requests.RequestException as exc:
        st.error(f"Konnte Notes nicht laden: {exc}")
        return

    if not notes:
        st.write("Noch keine Notes vorhanden.")
        return

    labels = [f"#{note['id']} - {note['title']}" for note in notes]
    selected_label = st.selectbox("Note auswaehlen", options=labels)
    selected_id = int(selected_label.split(" - ", maxsplit=1)[0].replace("#", ""))
    selected_note = next(note for note in notes if note["id"] == selected_id)

    st.markdown(f"**Titel:** {selected_note['title']}")
    st.markdown(f"**Kategorie:** {selected_note['category']}")
    st.markdown(f"**Tags:** {', '.join(selected_note.get('tags', [])) or '-'}")
    st.markdown("**Inhalt:**")
    st.write(selected_note["content"])


st.set_page_config(page_title="Notes Frontend", page_icon="📝", layout="wide")
st.title("Day 7: Streamlit Frontend")

st.markdown(
    "App für Day 7 🤙🤙: \n"
    "1) Streamlit Test mit externer API \n"
    "2) Frontend fuer die Notes API"
)

notes_api_base_url = st.sidebar.text_input(
    "Notes API Base URL",
    value=DEFAULT_NOTES_API_BASE_URL,
)
st.sidebar.caption("Beispiel: http://127.0.0.1:8000")

col_left, col_right = st.columns([1, 1])

with col_left:
    render_no_demo()

with col_right:
    st.subheader("Teil B: Notes API Frontend")
    st.caption(f"Backend aktuell: {notes_api_base_url}")
    render_create_note_form(notes_api_base_url)
    st.divider()
    render_notes_list(notes_api_base_url)

with st.expander("Session State"):
    st.write(st.session_state)
