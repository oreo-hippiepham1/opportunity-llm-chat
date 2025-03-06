from langchain_openai import ChatOpenAI

from .llm import get_llm, basic_chat
from .prompt import PROMPT_LETTER_GEN_V1

import streamlit as st

def generate_cover_letter(llm: ChatOpenAI,
                          cv_text: str,
                          letter_text: str,
                          opp_desc_text: str,
                          additional_reqs_text: str) -> dict:
    """
    Orchestrates the generation of a motivation letter,
        given a CV and a base motivational letter, a opportunity description,
        and any additional requests.
    """
    result = {
        'content': {}
    }

    if cv_text == "":
        st.warning("Please upload CV to generate the cover letter.")
    elif letter_text == "":
        st.warning("Please upload motivational letter to generate the cover letter.")
    elif opp_desc_text == "":
        st.warning("Please provide an opportuniy description to generate the cover letter.")
    else:
        with st.spinner("Generating cover letter..."):
            try:
                sys_prompt = PROMPT_LETTER_GEN_V1.format(cv_data=cv_text,
                                                        letter_data=letter_text,
                                                        opp_desc=opp_desc_text,
                                                        additional_reqs=additional_reqs_text)
                response = basic_chat(sys_prompt, llm)
                # updates session_state with the generated cover letter
                st.session_state.cover_generated = response
                return response

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.cover_generated = None
                return result

    return result