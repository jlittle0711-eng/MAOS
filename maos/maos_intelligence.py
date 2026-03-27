
import os
import numpy as np

from maos.chunker import chunk_text
from maos.embeddings import load_embedder
from maos.vector_store import VectorStore


DOCS = r"C:\MakerHub\MAOS\documents"
INDEX = r"C:\MakerHub\MAOS\index\maos.index"


def ingest_documents(embedder,store):

    for file in os.listdir(DOCS):

        path = os.path.join(DOCS,file)

        if not file.endswith(".txt"):
            continue

        try:

            text=open(path,"r",errors="ignore").read()

            chunks=chunk_text(text)

            embeddings=embedder.encode(chunks)

            store.add(embeddings,chunks)

        except:
            pass


def search_loop(store,embedder):

    print("")
    print("MAOS Intelligence Ready")
    print("Type a search query or 'exit'")
    print("")

    while True:

        q=input("Search MAOS > ")

        if q=="exit":
            break

        emb=np.array(embedder.encode([q])).astype("float32")

        if store.index is None:
            print("No documents indexed yet.")
            continue

        D,I=store.index.search(emb,5)

        for i in I[0]:

            if i < len(store.metadata):

                print("")
                print(store.metadata[i])


def main():

    embedder=load_embedder("all-MiniLM-L6-v2")

    store=VectorStore(INDEX)

    ingest_documents(embedder,store)

    store.save()

    search_loop(store,embedder)



if __name__=="__main__":
    main()

