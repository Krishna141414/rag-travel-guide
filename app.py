"""Local showcase server: serves web/ and a live POST /api/ask that runs the real RAG pipeline."""
import difflib

from flask import Flask, jsonify, request, send_from_directory

import rag

app = Flask(__name__, static_folder=None)
EXCERPT = 420  # characters of the article shown in the "raw vs cleaned" step


def ingest_view(title):
    """Raw vs cleaned opening of an article, as segments [text, removed?] so the page can strike out what cleaning dropped."""
    raw = next(a["text"] for a in rag.load_raw() if a["title"] == title)[:EXCERPT]
    clean = rag.clean_text(raw)
    segs = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, raw, clean, autojunk=False).get_opcodes():
        if op == "equal":
            segs.append([raw[i1:i2], False])
        else:
            if i2 > i1:
                segs.append([raw[i1:i2], True])
            if j2 > j1 and op == "replace":
                segs.append([clean[j1:j2], False])
    return {"title": title, "raw": raw, "clean": clean, "segments": segs}


def corpus_stats():
    raw, clean = rag.load_raw(), rag.load_articles()
    _, chunks = rag.load_index()
    return {"articles": len(raw), "raw_chars": sum(len(a["text"]) for a in raw),
            "clean_chars": sum(len(a["text"]) for a in clean), "chunks": len(chunks),
            "avg_chunk": round(sum(len(c["text"]) for c in chunks) / len(chunks)),
            "chunk_size": rag.CHUNK_SIZE, "overlap": rag.OVERLAP, "dim": 384, "k": rag.TOP_K,
            "embed_model": rag.EMBED_MODEL, "llm": rag.LLM_MODEL, "threshold": rag.THRESHOLD}


def full_answer(question):
    """rag.answer() + what the showcase page needs to explain each step."""
    r = rag.answer(question)
    _, chunks = rag.load_index()
    top = r["sources"][0]
    r["ingest"] = ingest_view(top["title"])
    r["chunking"] = {"article_chunks": sum(c["title"] == top["title"] for c in chunks), "example": top}
    return r


@app.get("/")
def home():
    return send_from_directory("web", "index.html")


@app.get("/<path:path>")
def files(path):
    return send_from_directory("web", path)


@app.get("/api/health")
def health():
    return jsonify(ok=True)


@app.post("/api/ask")
def api_ask():
    q = (request.get_json(silent=True) or {}).get("question", "").strip()[:300]
    if not q:
        return jsonify(error="question is required"), 400
    return jsonify(full_answer(q))


if __name__ == "__main__":
    rag.load_index(), rag.llm()                                       # load models once, before the first request
    print("Open http://127.0.0.1:5000")
    app.run(port=5000, debug=False)
