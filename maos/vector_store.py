import faiss
import numpy as np
import os

class VectorStore:

    def __init__(self,path):

        self.path=path
        self.metadata=[]

        if os.path.exists(path):
            self.index=faiss.read_index(path)
        else:
            self.index=None

    def add(self,embeddings,meta):

        embeddings=np.array(embeddings).astype("float32")

        if self.index is None:
            self.index=faiss.IndexFlatL2(embeddings.shape[1])

        self.index.add(embeddings)
        self.metadata.extend(meta)

    def save(self):

        faiss.write_index(self.index,self.path)
