"""Quick check: 7 answerable + 3 unanswerable questions -> results.md (+ results.json for the showcase page)."""
import json
import re
import time

import rag

# (question, expected article or None if the documents can't answer it)
TESTS = [
    ("Which emperor built the Taj Mahal?", "Agra"),
    ("What can you see in Kaziranga National Park?", "Kaziranga National Park"),
    ("Why is Rishikesh called the yoga capital of the world?", "Rishikesh"),
    ("When did Goa become part of India?", "Goa"),
    ("What is the Golden Temple in Amritsar?", "Amritsar"),
    ("What are the Ajanta Caves known for?", "Ajanta Caves"),
    ("Which city has a famous palace lit up during Dasara?", "Mysore"),
    ("What is the capital of Brazil?", None),
    ("Who is the current CEO of Tesla?", None),
    ("How tall is Mount Everest?", None),
]


def main():
    rag.load_index(), rag.llm(), rag.embed(["warm up"])               # load models first so timings are fair
    rows = []
    for q, expected in TESTS:
        t = time.perf_counter()
        r = rag.answer(q)
        secs = time.perf_counter() - t
        titles = [s["title"] for s in r["sources"]]
        rows.append({"question": q, "expected": expected or "(not in documents)", "top_sources": titles,
                     "best_score": r["best_score"], "status": r["status"], "llm_called": r["llm_called"],
                     "retrieval_hit": expected in titles if expected else None,
                     "correct": (r["status"] == "answered") if expected else (r["status"] == "not_found"),
                     "llm_cited": bool(re.search(r"\[\d\](?!\*)", r["answer"])) if r["status"] == "answered" else None,
                     "answer": r["answer"], "seconds": round(secs, 2)})
        print(f"{secs:5.1f}s {r['status']:9} {r['best_score']:.3f} {q}")

    ans = [x for x in rows if x["expected"] != "(not in documents)"]
    una = [x for x in rows if x["expected"] == "(not in documents)"]
    cited = [x for x in ans if x["llm_cited"] is not None]
    summary = {"retrieval_hit": sum(x["retrieval_hit"] for x in ans), "n_answerable": len(ans),
               "answered": sum(x["correct"] for x in ans),
               "not_found_correct": sum(x["correct"] for x in una), "n_unanswerable": len(una),
               "llm_cited": sum(x["llm_cited"] for x in cited), "n_cited_checked": len(cited),
               "avg_seconds": round(sum(x["seconds"] for x in rows) / len(rows), 2),
               "avg_seconds_answered": round(sum(x["seconds"] for x in ans) / len(ans), 2),
               "avg_seconds_refused": round(sum(x["seconds"] for x in una) / len(una), 3),
               "threshold": rag.THRESHOLD, "k": rag.TOP_K}
    json.dump({"summary": summary, "rows": rows}, open("results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    s = summary
    md = ["# Evaluation results", "",
          f"Top-k = {s['k']}, threshold = {s['threshold']}, LLM = {rag.LLM_MODEL} on CPU.", "",
          "| Metric | Result |", "|---|---|",
          f"| Retrieval hit (expected article in top-3) | {s['retrieval_hit']}/{s['n_answerable']} |",
          f"| Answerable questions answered | {s['answered']}/{s['n_answerable']} |",
          f"| Unanswerable correctly refused (\"not found\") | {s['not_found_correct']}/{s['n_unanswerable']} |",
          f"| Answers where the LLM wrote its own citation | {s['llm_cited']}/{s['n_cited_checked']} |",
          f"| Avg response time (all) | {s['avg_seconds']} s |",
          f"| Avg time, answered (LLM called) | {s['avg_seconds_answered']} s |",
          f"| Avg time, refused below threshold (no LLM) | {s['avg_seconds_refused']} s |", "",
          "| Question | Expected | Top sources | Best score | Status | OK | Time |", "|---|---|---|---|---|---|---|"]
    for x in rows:
        md.append(f"| {x['question']} | {x['expected']} | {', '.join(x['top_sources'])} | {x['best_score']:.3f} | "
                  f"{x['status']} | {'yes' if x['correct'] and x['retrieval_hit'] is not False else 'no'} | {x['seconds']} s |")
    md += ["", "## Answers", ""] + [f"- **{x['question']}** {x['answer']}" for x in rows]
    md += ["", "`[n]*` = citation added automatically by word overlap because the model left that sentence uncited."]
    open("results.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
