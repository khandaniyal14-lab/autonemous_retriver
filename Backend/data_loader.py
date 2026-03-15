# data_loader.py
from docx import Document

def load_documents(path="../sample.docx", chunk_size=500, chunk_overlap=100):
    """
    Load DOCX and split text into overlapping chunks manually.
    """
    # Load DOCX
    doc = Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    text = text.replace("\n", " ")  # flatten paragraphs

    # Split text into overlapping chunks
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap

    return chunks