import pdfplumber
import os

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def load_all_pdfs(pdf_dir):
    all_texts = []
    pdf_names = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_dir, filename)
            text = extract_text_from_pdf(path)
            all_texts.append(text)
            pdf_names.append(filename)
    return pdf_names, all_texts