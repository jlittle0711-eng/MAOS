import numpy as np

def search_loop(store,embedder):

    print("MAOS ready")

    while True:

        q=input("Search MAOS > ")

        if q=="exit":
            break

        emb=np.array(embedder.encode([q])).astype("float32")

        D,I=store.index.search(emb,5)

        for i in I[0]:

            if i < len(store.metadata):
                print(store.metadata[i])
