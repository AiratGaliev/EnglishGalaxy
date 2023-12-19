import streamlit as st

from config.Config import Config
from logic.utils import get_access_token, parse_numeric_array, generate_cards

levels_list: list[str] = Config.LEVELS_LIST.value
american_accent: bool = Config.AMERICAN_ACCENT.value
british_accent: bool = Config.BRITISH_ACCENT.value
collection_media = Config.COLLECTION_MEDIA.value
documents = Config.DOCUMENTS.value
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
    is_generate_lessons = False
    access_token = get_access_token(email, password)
    lessons: list[int] = parse_numeric_array("1..50")
    regenerate_exercise: int = 0
    is_generate_all_levels = st.checkbox("Generate all levels", value=True)
    if not is_generate_all_levels:
        is_generate_texts_of_all_levels = st.checkbox("Generate texts of all levels", value=True)
    if not (is_generate_all_levels or is_generate_texts_of_all_levels):
        levels_list = [st.selectbox("Select levels", levels_list)]
        is_generate_lessons = st.checkbox("Generate lessons", value=True)
        genre = st.radio("Select lessons", ["Some", "One"])
        if genre == "Some":
            lessons = st.slider('Select a range of generate lessons', 1, 50, (1, 50))
            start, end = lessons
            lessons = list(range(start, end + 1))
        else:
            lessons = [st.number_input("Select generate lesson", value=1, min_value=1, max_value=50, step=1)]
            regenerate_exercise = st.number_input("Regenerate exercise", value=1, min_value=1, step=1)
    start_btn = st.button('Start', type="primary", on_click=click_button, disabled=st.session_state.clicked)
    if start_btn:
        with st.status("Operation in progress. Please wait.") as status:
            for level in levels_list:
                for lesson in lessons:
                    generate_cards(level, lesson, regenerate_exercise, is_generate_lessons, american_accent,
                                   british_accent,
                                   collection_media, documents, access_token)
            status.update(label="Operation completed", state="complete")
            st.session_state.clicked = False
