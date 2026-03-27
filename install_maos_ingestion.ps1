Write-Host "Installing MAOS ingestion engine..."

# install Python packages
pip install watchdog pymupdf pytesseract opencv-python

# install Tesseract OCR
$tesseract = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe"
$out = "tesseract_installer.exe"

Invoke-WebRequest $tesseract -OutFile $out
Start-Process $out -Wait

# create PDF ingestion module
@"
import fitz
from maos.chunker import chunk_text

def read_pdf(path):

    text=""

    doc=fitz.open(path)

    for page in doc:
        text+=page.get_text()

    return chunk_text(text)
"@ | Set-Content "maos\ingest_pdf.py"

# create OCR ingestion module
@"
import pytesseract
import cv2
from maos.chunker import chunk_text

def read_image(path):

    img=cv2.imread(path)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    text=pytesseract.image_to_string(gray)

    return chunk_text(text)
"@ | Set-Content "maos\ingest_ocr.py"

# create document watcher
@"
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchHandler(FileSystemEventHandler):

    def __init__(self,callback):
        self.callback=callback

    def on_created(self,event):

        if not event.is_directory:
            self.callback(event.src_path)

def start_watcher(folder,callback):

    handler=WatchHandler(callback)

    observer=Observer()
    observer.schedule(handler,folder,recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
"@ | Set-Content "maos\document_watcher.py"

Write-Host "MAOS ingestion upgrade installed"
