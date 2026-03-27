import sqlite3
from signal_processor import apply_signals
from decision_engine import evaluate_grant

DB_PATH = "C:\\MakerHub\\MAOS\\grants.db"


# =========================
# DATABASE LAYER
# =========================
def fetch_grants():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, agency, funding, deadline, location, keywords, source, type, score
        FROM grants
    """)

    rows = cursor.fetchall()
    conn.close()

    grants = []

    for row in rows:
        grants.append({
            "title": row[0],
            "agency": row[1],
            "funding": row[2],
            "deadline": row[3],
            "location": row[4],
            "keywords": row[5],
            "source": row[6],
            "type": row[7],
            "score": row[8] or 0
        })

    return grants


# =========================
# PIPELINE STAGES
# =========================
def run_full_pipeline():
    print("\n=== RUNNING MAOS PIPELINE ===\n")

    grants = fetch_grants()

    if not grants:
        print("No records found in database.\n")
        return

    results = []

    for grant in grants:
        # Stage 1 — Signal Processing
        modified_score, flags, context = apply_signals(grant)

        # Stage 2 — Decision Engine
        result = evaluate_grant(grant, modified_score, flags, context)

        results.append(result)

    # Stage 3 — Output
    for result in results:
        print("----------------------------------------")
        print(f"TITLE: {result['title']}")
        print(f"AGENCY: {result['agency']}")
        print(f"SCORE: {result['score']}")
        print()
        print(f"PRIORITY: {result['priority']}")
        print(f"ACTION: {result['action']}")
        print()
        print("FLAGS:")
        if result["flags"]:
            for flag in result["flags"]:
                print(f"- {flag}")
        else:
            print("- NONE")
        print()
        print("REASON:")
        print(result["reason"])
        print("----------------------------------------")

    print("\n=== PIPELINE COMPLETE ===\n")


def semantic_search():
    print("\n[Semantic Search Placeholder]")
    print("→ Will connect to vector_search.py in next phase.\n")


def show_topics():
    print("\n[Topics Placeholder]")
    print("→ Will connect to knowledge.json / tracking system.\n")


# =========================
# CONTROLLER LOOP
# =========================
def main():
    while True:
        print("\nMAOS CONTROLLER\n")
        print("1 - Run Full Pipeline")
        print("2 - Semantic Search")
        print("3 - Show Topics")
        print("4 - Exit\n")

        choice = input("Select option: ").strip()

        if choice == "1":
            run_full_pipeline()
        elif choice == "2":
            semantic_search()
        elif choice == "3":
            show_topics()
        elif choice == "4":
            print("\nExiting MAOS.\n")
            break
        else:
            print("\nInvalid selection.\n")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()