import streamlit as st

from src.data_processing import parse_pdf, parse_docx, extract_full_text_from_chunks

from src.ui import render_file_uploaders
from src.ui import preview_content_section

from src.core import get_llm, basic_chat, PROMPT_PRE_ANALYSIS_V1, PROMPT_LETTER_GEN_V1, generate_cover_letter, generate_pre_analysis


st.set_page_config(
        page_title="Job App made easy",
        page_icon="🐳",
        layout='wide'
    )
st.title("Resume App Assistant 🕵️‍♂️")

st.markdown(""
"In the current economy, job or scholarship opportunities are endless, but with that, comes the additional burden of hand-crafting a custom cover letter for each post. It gets even worse, when you want to draft a cold email to the recruiter, for a minor mistake or miscommunication can have dire consequences."

"\n\nThis app is designed to help alleviate that process, by scraping off hopefully a few minutes from your application process, and freeing up your brain power."
"\n\nThe app may be a bit wonky at times, but it does what it does - even saving 1 minute for each application, goes a long way!"
"\n\n"
"👈 **Open left sidebar to change model! (recommended - start with 4o-mini)**"
)


class ResumeAssistant():
    def __init__(self):
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

        selected_model = st.sidebar.selectbox("Choose the model",
                                                ['gpt-4o-mini', 'o1-mini'],
                                                index=0,
                                                key='model_type')
        self.llm = get_llm()

    def upload_cv_and_letter(self):
        # CV UPLOAD WIDGET
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

    def pre_analysis(self):
        if 'analysis_result' not in st.session_state:
            st.session_state.analysis_result = None

        analyze_button = st.button("Analyze CV and Letter 📈")

        if analyze_button:
            if st.session_state.get('cv_data') and st.session_state.get('letter_data'):
                with st.spinner("Analysis in progress..."):
                    response = generate_pre_analysis(st.session_state['cv_data'],
                                                        st.session_state['letter_data'],
                                                        self.llm)
            else:
                st.warning("Please upload CV and letter first to perform the analysis!")

        if 'analysis_result' in st.session_state and st.session_state['analysis_result']:
            container = st.container(height=200, border=True)
            container.write(st.session_state['analysis_result'].content)
        else:
            st.write("Generate a quick analysis, or skip this step.")

    def opp_process(self):
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

    def add_reqs(self):
        additional_req_data = ""
        additional_req = st.text_area("Any additional requirements you want to add for the cover letter / cold email...",
                                    height=200)
        if additional_req:
            additional_req_data = extract_full_text_from_chunks([additional_req])
            return additional_req_data


    def final_gen(self):
        if 'cover_generated' not in st.session_state:
            st.session_state.cover_generated = None

        additional_req_data = self.add_reqs()

        cover_gen_button = st.button("GENERATE LETTER OR EMAIL 🚀")

        if cover_gen_button:
            response = generate_cover_letter(self.llm,
                                             st.session_state['cv_data'],
                                             st.session_state['letter_data'],
                                             st.session_state['opp_desc_data'],
                                             additional_req_data)

        if 'cover_generated' in st.session_state and st.session_state['cover_generated']:
            st.write(st.session_state['cover_generated'].content)


    def main(self):
        st.header("Your Main Uploads 📤")
        st.markdown("**1. Upload your CV and a base cover letter.**\n\n")
        self.upload_cv_and_letter()

        st.header("Pre Analysis 📊")
        st.markdown("**2. [Optional] Generate a pre-analysis of your profile's strength and weaknesses.**\n\n")
        self.pre_analysis()

        st.header("Opportunity Uploads")
        st.markdown("**3. Paste, or upload that job / scholarship etc.. description.**\n\n")
        self.opp_process()

        st.header("Generation! 📝")
        st.markdown("**4. Write any additional requests you would like to have (e.g. Draft a cold emailing focusing on ....) and Generate!**\n\n")
        self.final_gen()


if __name__ == "__main__":
    bot = ResumeAssistant()
    bot.main()