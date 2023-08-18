from langchain.text_splitter import RecursiveCharacterTextSplitter
# from load_file import 
from django.utils import timezone
import io
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from .handle_file import upload_docx_file, upload_pdf_file, upload_pptx_file, get_docx_text, get_pptx_text, get_pdf_text
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
    )
    split_texts = text_splitter.create_documents([text])
    return split_texts


def get_vector(text) -> ndarray:
    vector = model.encode(text)
    return vector

def handle_upload(file, file_type):
    if file_type == 'pdf':
        pdf_reader = upload_pdf_file(file)
        return get_pdf_text(pdf_reader)
    elif file_type == 'docx':
        docx_reader = upload_docx_file(file)
        return get_docx_text(docx_reader)
    elif file_type == 'pptx':
        pptx_file = upload_pptx_file(file)
        return get_pptx_text(pptx_file)
    else:
        return None




