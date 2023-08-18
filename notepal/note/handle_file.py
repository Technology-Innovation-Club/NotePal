from pypdf import PdfReader
import docx
from pptx import Presentation
import pandas as pd
import numpy as np
import re


# upload DOCX file
def upload_docx_file(docx_file):
    docx_reader = docx.Document(docx_file)
    return docx_reader

# get text from DOCX file
def get_docx_text(docx_reader):
    fullText = []
    for para in docx_reader.paragraphs:
            fullText.append(para.text)
    doc_text = '\n'.join(fullText)
    cleaned_text = clean_and_convert_to_utf8(doc_text)
    return cleaned_text
