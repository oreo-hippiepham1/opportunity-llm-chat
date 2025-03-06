import streamlit as st

from src.data_processing import parse_pdf, parse_docx, extract_full_text_from_chunks

from src.ui import render_file_uploaders
from src.ui import preview_content_section

from src.core import get_llm, basic_chat, PROMPT_PRE_ANALYSIS_V1, PROMPT_LETTER_GEN_V1, generate_cover_letter, generate_pre_analysis


def main():
    st.set_page_config(
        page_title="Job App made easy",
        page_icon="🐳",
        layout='wide'
    )
    st.title("Resume App Assistant 🕵️‍♂️")

    # Initialize session states
    if "cv_data" not in st.session_state:
        st.session_state.cv_data = None  # Store parsed data directly
    if "letter_data" not in st.session_state:
        st.session_state.letter_data = None
    if "opp_desc_data" not in st.session_state:
        st.session_state.opp_desc_data = None
    if "additional_req_data" not in st.session_state:
        st.session_state.additional_req_data = None
    if "model_type" not in st.session_state:
        st.session_state.model = None
    if "current_model" not in st.session_state:
        st.session_state.current_model = None

    # Choose model
    selected_model = st.sidebar.selectbox("Choose the model",
                                          ['gpt-4o-mini', 'o1-mini'],
                                          index=0,
                                          key='model_type')
    llm = get_llm() # everytime an input widget is changed, ST will re-run the whole script (UNLESS session_state is used)

    # CV UPLOAD WIDGET
    st.subheader("Your Uploads 📤")
    uploads = render_file_uploaders()
    col1, col2 = st.columns(2)
    if uploads['cv'] and not st.session_state['cv_data']:
        with st.spinner("Parsing the PDF..."):
            try:
                cv_chunks = parse_pdf(uploads['cv'])
                col1.success("CV Uploaded ✅")
                # Convert the chunks into 1 full string, and stores in session_state
                st.session_state['cv_data'] = extract_full_text_from_chunks(cv_chunks)
            except Exception as e:
                col1.error(f"Error parsing the PDF: {str(e)}")

    # MOTIVATIONAL LETTER UPLOAD WIDGET
    if uploads['letter'] and not st.session_state['letter_data']:
        with st.spinner("Parsing the DOCX..."):
            try:
                letter_chunks = parse_docx(uploads['letter'])
                col2.success("Letter Uploaded ✅")
                # Convert the chunks into 1 full string, and stores in session_state
                st.session_state['letter_data'] = extract_full_text_from_chunks(letter_chunks)
            except Exception as e:
                col2.error(f"Error parsing the DOCX {str(e)}")


    # Pre-Analysis Results
    st.subheader("Pre-Analysis 📊")
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    analyze_button = st.button("Analyze CV and Letter 📈")
    container = st.container(height=250, border=True)

    if analyze_button:
        if st.session_state.get('cv_data') and st.session_state.get('letter_data'):
            with st.spinner("Analysis in progress..."):
                response = generate_pre_analysis(st.session_state['cv_data'],
                                                    st.session_state['letter_data'],
                                                    llm)
        else:
            container.warning("Please upload CV and letter first to perform the analysis!")

    if 'analysis_result' in st.session_state and st.session_state['analysis_result']:
        container.write(st.session_state['analysis_result'].content)


    # Job description analysis
    st.subheader("Generation! 📝")

    # Opportunity Uploads
    if 'opp_desc_data' not in st.session_state:
        st.session_state['opp_desc_data'] = None

    opp_desc_type = st.selectbox(label="How do you want to upload opportunity desc?",
                                 options=['Text', 'PDF', 'DOCX'],
                                 index=0)

    if opp_desc_type == 'Text':
        opp_desc = st.text_area(label="Paste the opportunity here...",
                                height=250)

        if opp_desc:
            st.session_state['opp_desc_data'] = extract_full_text_from_chunks([opp_desc])

    elif opp_desc_type == 'PDF':
        opp_desc_upload = st.file_uploader("Opportunity Flyer (PDF)", type=['pdf'])
        if opp_desc_upload:
            try:
                opp_desc_chunks = parse_pdf(opp_desc_upload)
                st.session_state['opp_desc_data'] = extract_full_text_from_chunks(opp_desc_chunks)
            except Exception as e:
                st.error(f"Something wrong with you uploads")

    else:
        opp_desc_upload = st.file_uploader("Opportunity Flyer (DOCX)", type=['docx'])
        if opp_desc_upload:
            try:
                opp_desc_chunks = parse_docx(opp_desc_upload)
                st.session_state['opp_desc_data'] = extract_full_text_from_chunks(opp_desc_chunks)
            except Exception as e:
                st.error(f"Something wrong with you uploads")


    additional_req_data = ""
    additional_req = st.text_area("Any additional requirements you want to add for the cover letter / cold email...",
                                  height=200)
    if additional_req:
        additional_req_data = extract_full_text_from_chunks([additional_req])

    if 'cover_generated' not in st.session_state:
        st.session_state.cover_generated = None

    cover_gen_button = st.button("GENERATE LETTER OR EMAIL 🚀")
    if cover_gen_button:
        response = generate_cover_letter(llm,
                                         st.session_state['cv_data'],
                                         st.session_state['letter_data'],
                                         st.session_state['opp_desc_data'],
                                         additional_req_data)

    if 'cover_generated' in st.session_state and st.session_state['cover_generated']:
        st.write(st.session_state['cover_generated'].content)

if __name__ == "__main__":
    main()