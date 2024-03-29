import os

import streamlit as st

from config.Config import Config
from logic.utils import get_access_token, parse_numeric_array, generate_cards, get_file_paths, clean_up_duplicates

levels_list: list[str] = Config.LEVELS_LIST.value
folders = [level.upper() for level in levels_list]
documents = Config.DOCUMENTS.value
folder_paths: list[str] = [os.path.join(documents + "CSV", folder) for folder in folders]
file_paths: list[str] = get_file_paths(folder_paths)
clean_up_duplicates(file_paths)
american_accent: bool = Config.AMERICAN_ACCENT.value
british_accent: bool = Config.BRITISH_ACCENT.value
collection_media = Config.COLLECTION_MEDIA.value
email = Config.EMAIL.value
password = Config.PASSWORD.value

if __name__ == '__main__':

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False


    def click_button():
        st.session_state.clicked = True


    st.set_page_config(
        page_title="English Galaxy",
        page_icon="card_file_box",
    )
    st.title("Generate Anki Cards")
    is_generate_texts_of_all_levels = False
    access_token = get_access_token(email, password)
    lessons: list[int] = parse_numeric_array("1..50")
    regenerate_exercise: int = 0
    is_american_accent = st.checkbox("American accent", value=american_accent)
    is_british_accent = st.checkbox("British accent", value=british_accent, disabled=True)
    is_generate_all_text_to_audio = st.checkbox("Generate all levels text to audio", value=False)
    if not is_generate_all_text_to_audio:
        is_generate_texts_of_all_levels = st.checkbox("Generate texts of all levels", value=True)
    if not (is_generate_all_text_to_audio or is_generate_texts_of_all_levels):
        levels_list = [st.selectbox("Select levels", levels_list)]
        is_generate_all_text_to_audio = st.checkbox("Generate lessons", value=True)
        genre = st.radio("Select lessons", ["Some", "One"])
        if genre == "Some":
            lessons = st.slider('Select a range of generate lessons', 1, 50, (1, 50))
            start, end = lessons
            lessons = list(range(start, end + 1))
        else:
            lessons = [st.number_input("Select generate lesson", value=1, min_value=1, max_value=50, step=1)]
            regenerate_exercise = st.number_input("Regenerate exercise", value=1, min_value=1, step=1)
    start_btn = st.button('🚩 Start', type="secondary", on_click=click_button, disabled=st.session_state.clicked)
    if start_btn:
        with st.status("🚧 Operation in progress. Please wait. 🚧") as status:
            for level in levels_list:
                for lesson in lessons:
                    generate_cards(level, lesson, regenerate_exercise, is_generate_all_text_to_audio,
                                   is_american_accent, is_british_accent, collection_media, documents, access_token)
            status.update(label="🏁 Operation completed 🏁", state="complete")
            st.session_state.clicked = False
