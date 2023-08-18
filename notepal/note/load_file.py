from .handle_file import upload_docx_file, upload_pdf_file, upload_pptx_file, get_docx_text, get_pptx_text, get_pdf_text
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




