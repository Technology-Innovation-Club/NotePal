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

# Upload PPTX file
def upload_pptx_file(pptx_file):
    prs = Presentation(pptx_file)
    return prs

# Get text from PPTX file
def get_pptx_text(prs):
    text_runs = []

    # pptx reads in all text for detected shapes in PowerPoint
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    text_runs.append(run.text)

    pptx_text = " ".join(text_runs)
    pptx_text_clean = re.sub(r'[^a-zA-Z0-9_.\s]+', '', pptx_text)
    
    pptx_cleaned_text = clean_and_convert_to_utf8(pptx_text_clean)
    return pptx_cleaned_text


