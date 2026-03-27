import os
from maos.chunker import chunk_text
from maos.embeddings import load_embedder
from maos.vector_store import VectorStore

def ingest_documents(config):

    embedder=load_embedder(config["embedding_model"])

    index_path=os.path.join(config["index_folder"],"maos.index")

    store=VectorStore(index_path)

    docs=config["documents_folder"]

    for file in os.listdir(docs):

        path=os.path.join(docs,file)

        try:

            with open(path,"r",errors="ignore") as f:
                text=f.read()

        except:
            continue

        print("Processing:",file)

        chunks=chunk_text(text)

        embeddings=embedder.encode(chunks)

        store.add(embeddings,chunks)

    store.save()

    return store,embedder
