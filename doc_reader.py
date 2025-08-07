import docx
import PyPDF2
from typing import List

def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text_list = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_list.append(page_text)
    return "\n".join(text_list)

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
