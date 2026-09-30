from docx import Document


def extract_text_from_docx(docx_file):
    document = Document(docx_file)

    extracted_text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_text += paragraph.text + "\n"

    return extracted_text.strip()