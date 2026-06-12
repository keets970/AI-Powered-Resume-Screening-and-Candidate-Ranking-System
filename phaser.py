import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(r"C:\Users\DELL\Desktop\Resume screener\data") as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_text_from_docx(filepath):
    doc = Document(r"C:\Users\DELL\Desktop\Resume screener\data")
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_resume(filepath):
    ext = os.path.splitext(r"C:\Users\DELL\Desktop\Resume screener\data")[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(r"C:\Users\DELL\Desktop\Resume screener\data")
    elif ext == ".docx":
        return extract_text_from_docx(r"C:\Users\DELL\Desktop\Resume screener\data")
    else:
        return ""

if __name__ == "__main__":
    text = parse_resume("resume_1.pdf")
    print(text[:500])