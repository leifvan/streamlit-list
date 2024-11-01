import streamlit as st
from utils import Database

db = Database()

st.title("100. Geburtstag")
st.write("Was ich mitbringe")

@st.fragment(run_every="10s")
def data_container():
    with st.spinner("Lade Daten..."):
        df = db.get_items()

    for row in df.itertuples():
        with st.container(border=True):
            col1, col2 = st.columns([11, 1])
            col1.write(f"**{row.name}**: {row.text}")
            if col2.button(label="", key=f"delete_{row.id}", icon=":material/delete:"):

                @st.dialog(title="Eintrag löschen")
                def confirm(id, name, text):
                    st.write("Bist du dir sicher, dass du diesen Eintrag löschen möchtest?")
                    with st.container(border=True):
                        st.write(f"**{name}**: {text}")
                    
                    col1, col2 = st.columns([1, 1])
                    if col1.button("Löschen", type='primary', use_container_width=True):
                        db.delete_item(id)
                        st.rerun()
                    if col2.button("Abbrechen", use_container_width=True):
                        st.rerun()

                confirm(row.id, row.name, row.text)

                

data_container()

col1, col2 = st.columns([2, 10])
name_input = col1.text_input(
    label="",
    key="name_input",
    placeholder="Mein Name",
    max_chars=128,
    label_visibility='collapsed'
)
text_input = col2.chat_input(
    key="text_input",
    placeholder="Was ich mitbringe",
    max_chars=1024,
)

if text_input:
    if not name_input:
        st.error("Fehler: Du musst deinen Namen eingeben, um etwas zur Liste hinzuzufügen.")
    else:
        db.add_item(name_input or name_input, text_input)
        st.rerun()