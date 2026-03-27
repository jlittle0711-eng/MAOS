import fitz
from maos.chunker import chunk_text

def read_pdf(path):

    text=""

    doc=fitz.open(path)

    for page in doc:
        text+=page.get_text()

    return chunk_text(text)
