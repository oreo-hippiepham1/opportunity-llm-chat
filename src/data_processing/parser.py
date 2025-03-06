from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
import tempfile

import streamlit as st

def parse_pdf(uploaded_file: "UploadedFile") -> list:
    """
    Parse the uploaded PDF file and return the text content as chunks.
    """
    pages = None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.getvalue()) # writes the uploaded file bytes stream to temp

        temp_pdf_path = temp_pdf.name
        loader = PyPDFLoader(temp_pdf_path)

        pages = loader.load_and_split() # extracts PDF content, splits it into Document objects

    return [p.page_content for p in pages] # chunks


def parse_docx(uploaded_file: "UploadedFile") -> list:
    """
    Parse the uploaded DOCX file and return the text content as chunks.
    """
    pages = None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        temp_docx.write(uploaded_file.getvalue())

        temp_docx_path = temp_docx.name
        loader = Docx2txtLoader(temp_docx_path)

        pages = loader.load_and_split()

    return [p.page_content for p in pages] # chunks


def extract_full_text_from_file(uploaded_file: "UploadedFile") -> str:
    """
    Extracts the full text content of the upload file.
    ONLY USE IF FILE IS SMALL ENOUGH (within avg LLM context window)
    """
    chunks = None
    if uploaded_file.type == 'pdf':
        chunks = parse_pdf(uploaded_file)

    elif uploaded_file.type == 'docx':
        chunks = parse_docx(uploaded_file)

    else:
        chunks = []

    return extract_full_text_from_chunks(chunks)


def extract_full_text_from_chunks(chunks: list) -> str:
    return '\n'.join(chunks)