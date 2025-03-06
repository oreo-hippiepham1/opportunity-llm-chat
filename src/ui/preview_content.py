import streamlit as st

def preview_content_section(chunks):
    st.text("Parsed Content Preview...")
    with st.expander("Click to expand"):
        for i, chunk in enumerate(chunks):
            st.write(f"Chunk {i + 1}")
            st.code(chunk, language="text")