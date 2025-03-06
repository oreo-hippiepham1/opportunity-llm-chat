from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, SystemMessage, HumanMessage

import streamlit as st

from .llm import get_llm, basic_chat
from .prompt import PROMPT_PRE_ANALYSIS_V1


def generate_pre_analysis(cv_data: str,
                 letter_data: str,
                 llm: ChatOpenAI
                 ) -> str:
    try:
        sys_prompt = PROMPT_PRE_ANALYSIS_V1.format(cv_data=cv_data,
                                                letter_data=letter_data)
        response = basic_chat(sys_prompt, llm)
        # updates session_state with the analysis result
        st.session_state.analysis_result = response

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.analysis_result = None

    return response