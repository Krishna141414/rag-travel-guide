"""Precompute web/demo_data.js so the showcase page works instantly without the model (also from file:// or a static host).
Run evaluate.py first (it writes results.json)."""
import inspect
import json
from pathlib import Path

import rag
from app import corpus_stats, full_answer

# example buttons: (label, what it demonstrates, question)
EXAMPLES = [
    ("Taj Mahal builder", "Answerable -> cited answer", "Which emperor built the Taj Mahal?"),
    ("Goa joins India", "LLM writes its own citation", "When did Goa become part of India?"),
    ("Kaziranga wildlife", "List answer from one source", "What can you see in Kaziranga National Park?"),
    ("Capital of Brazil", "Unanswerable -> refused, no LLM", "What is the capital of Brazil?"),
    ("Eiffel Tower in Shimla", "Passes threshold -> LLM says 'don't know'", "How tall is the Eiffel Tower in Shimla?"),
]
FINDINGS = [
    "Retrieval is the strong part: the expected article was in the top-3 sources for 7/7 answerable questions, usually in all three slots.",
    "The score threshold (0.50) refused all 3 out-of-scope questions in ~10 ms without calling the LLM. 'Capital of Brazil' still scores 0.47 because Goa's text mentions the Portuguese empire, so the margin is thin.",
    "The prompt's 'say you don't know' rule is a second guard: 'Eiffel Tower in Shimla' passes the threshold (0.55) but the LLM refuses instead of inventing a height.",
    "The 0.5B model answers correctly but writes its own [n] citation only 1/7 times; the rest are added by word overlap and marked [n]* so this is visible, not hidden.",
    "On CPU an answered question takes ~2-5 s once models are loaded; the first request also loads the models (~10-40 s).",
]


def main():
    results = json.loads(Path("results.json").read_text(encoding="utf-8"))
    data = {"stats": corpus_stats(), "findings": FINDINGS, "results": results,
            "examples": [{"label": lab, "hint": hint, "result": full_answer(q)} for lab, hint, q in EXAMPLES],
            "code": {f"rag.py :: {f.__name__}()": inspect.getsource(f)
                     for f in (rag.clean_text, rag.build_prompt, rag.answer, rag.add_citations)}}
    js = "window.DEMO = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    Path("web").mkdir(exist_ok=True)
    Path("web/demo_data.js").write_text(js, encoding="utf-8")
    print("wrote web/demo_data.js", len(js) // 1024, "KB")
    for ex in data["examples"]:
        r = ex["result"]
        print(f"{r['status']:9} {r['best_score']:.3f} {r['question']}\n   {r['answer']}")


if __name__ == "__main__":
    main()
