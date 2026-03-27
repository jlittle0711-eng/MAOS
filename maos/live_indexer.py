import os
import time
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from maos.chunker import chunk_text
from maos.embeddings import load_embedder
from maos.vector_store import VectorStore
from maos.ingest_pdf import read_pdf
from maos.ingest_ocr import read_image


DOCS = "documents"
INDEX = "index/maos.index"


class MAOSWatcher(FileSystemEventHandler):

    def __init__(self, embedder, store):
        self.embedder = embedder
        self.store = store

    def process(self, path):

        print(f"Ingesting: {path}")

        ext = os.path.splitext(path)[1].lower()

        try:

            if ext == ".txt":
                text = open(path,"r",errors="ignore").read()
                chunks = chunk_text(text)

            elif ext == ".pdf":
                chunks = read_pdf(path)

            elif ext in [".png",".jpg",".jpeg"]:
                chunks = read_image(path)

            else:
                print("Unsupported file")
                return

            embeddings = self.embedder.encode(chunks)
            self.store.add(embeddings,chunks)
            self.store.save()

            print("Indexed.")

        except Exception as e:
            print("Error:",e)


    def on_created(self,event):

        if event.is_directory:
            return

        time.sleep(1)
        self.process(event.src_path)



def start_maos():

    embedder = load_embedder("all-MiniLM-L6-v2")

    store = VectorStore(INDEX)

    handler = MAOSWatcher(embedder,store)

    observer = Observer()
    observer.schedule(handler,DOCS,recursive=False)

    observer.start()

    print("MAOS Live Indexing Started")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()



if __name__ == "__main__":
    start_maos()

