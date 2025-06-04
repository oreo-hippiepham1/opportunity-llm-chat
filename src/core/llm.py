from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, SystemMessage, HumanMessage

import streamlit as st


def get_llm():
    # fetch the API key from the secrets
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    # retrieve model from session state, default to gpt-4o-mini
    model = st.session_state.get("model_type", "gpt-4o-mini")

    # initialize LLM
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=model, temperature=1)

    return llm


def basic_chat(initial_system: str, llm: ChatOpenAI) -> dict:
    result = {"content": {}}
    if llm.model_name == "gpt-4o-mini":
        result = llm.invoke([SystemMessage(content=initial_system)])
    elif (
        llm.model_name == "o4-mini"
        or llm.model_name == "o3-mini"
        or llm.model_name == "gpt-4o"
    ):
        result = llm.invoke([HumanMessage(content=initial_system)])
    else:
        result["content"] = {llm.model_name: "Not Supported"}

    return result
