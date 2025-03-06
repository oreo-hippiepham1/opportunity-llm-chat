import streamlit as st

from src.data_processing import parse_pdf, parse_docx, extract_full_text_from_chunks

from src.ui import render_file_uploaders
from src.ui import preview_content_section

from src.core import get_llm, basic_chat, PROMPT_PRE_ANALYSIS_V1


def main():
    st.title("Education RAG Assistant 🕵️‍♂️")

    # CV UPLOAD WIDGET
    cv_upload = render_file_uploaders('pdf')

    if cv_upload['cv'] is not None:
        st.success("Content Uploaded ✅")
        with st.spinner("Parsing the PDF..."):
            cv_chunks = parse_pdf(cv_upload['cv'])
            st.sidebar.button("Quiz Bank for {book_name}")
            with st.sidebar.expander("Book Chapters:"):
                st.write("Chapter 1: ___")


        # Show content
        preview_content_section(cv_chunks)
        # st.text(extract_full_text_from_chunks(cv_chunks))

    # # MOTIVATIONAL LETTER UPLOAD WIDGET
    # letter_upload = render_file_uploaders('docx')

    # if letter_upload['letter'] is not None:
    #     st.success("Letter Uploaded ✅")
    #     with st.spinner("Parsing the DOCX..."):
    #         letter_chunks = parse_docx(letter_upload['letter'])

        # Show content
    #     preview_content_section(letter_chunks)

    # # Analysis button
    # if cv_upload and letter_upload:
    #     analize = st.button("Analysis 🚀")

    #     if analize:
    #         with st.spinner("Analysis in progress..."):
    #             cv_full = extract_full_text_from_chunks(cv_chunks)
    #             letter_full = extract_full_text_from_chunks(letter_chunks)
    #             prompt = PROMPT_PRE_ANALYSIS_V1.format(cv_data=cv_full,
    #                                                    letter_data=letter_full)

    #             llm = get_llm()
    #             response = basic_chat(prompt, llm)
    #             st.write(response)

    st.header("Quiz Session 📝")
    quiz_gen = st.button("Generate Quiz 🚀")

    # Job description analysis
    st.header("QnA Session 📝")
    prompt = st.chat_input("Ask me anything!")
    if prompt:
        with st.chat_message("user"):
            st.write(f"{prompt}")
        llm = get_llm()
        response = basic_chat(prompt, llm)
        with st.chat_message("bot"):
            st.write(f"{response}")



if __name__ == "__main__":
    main()