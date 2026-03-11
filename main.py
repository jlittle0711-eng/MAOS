from maos.config_loader import load_config, ensure_dirs
from maos.ingest_txt import ingest_documents
from maos.search_cli import search_loop

def main():

    config = load_config()
    ensure_dirs(config)

    store, embedder = ingest_documents(config)

    search_loop(store, embedder)

if __name__ == "__main__":
    main()
