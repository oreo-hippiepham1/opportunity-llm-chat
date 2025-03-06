import streamlit as st

def render_file_uploaders() -> dict:
    """
    Renders the file upload widget
    """
    col1, col2 = st.columns(2)
    uploads = {
        'cv': col1.file_uploader("CV (PDF)", type=["pdf"]),
        'letter': col2.file_uploader("Cover letter (DOCX)", type=["docx"])
    }

    if uploads['cv']:
        st.session_state['cv_data'] = None # reset previous data
    if uploads['letter']:
        st.session_state['letter_data'] = None

    return uploads