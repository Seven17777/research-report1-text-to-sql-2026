"""An illustrative SQLite counterexample, not an LLM benchmark reproduction."""
import json
import sqlite3
from pathlib import Path


def evaluate(scores):
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, score INTEGER NOT NULL)")
        db.executemany("INSERT INTO customers VALUES (?, ?)", list(enumerate(scores, start=1)))
        reference = db.execute("SELECT COUNT(*) FROM customers WHERE score >= 80").fetchone()[0]
        wrong = db.execute("SELECT COUNT(*) FROM customers WHERE score > 80").fetchone()[0]
        return {"scores": scores, "reference": reference, "wrong": wrong, "agreement": reference == wrong}


if __name__ == "__main__":
    results = [evaluate([60, 90]), evaluate([60, 80, 90])]
    assert results[0]["agreement"] is True
    assert results[1]["agreement"] is False
    destination = Path(__file__).resolve().parent/"results.json"
    destination.write_text(json.dumps(results, indent=2)+"\n", encoding="utf8")
    print(json.dumps(results, indent=2))
