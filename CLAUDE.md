# Task 8: RAG Travel Guide Q&A (VoidMain Internship)

## Goal
Brief: "Build an end-to-end RAG application grounded in external knowledge. Choose a practical document/knowledge-based problem. Implement ingestion, cleaning, chunking, embeddings, vector storage, retrieval, prompt construction and LLM response generation. Provide source/context references and appropriately handle unanswerable questions."
**Keep it SIMPLE: small Python modules + one simple local web page + README. Runs locally only (no deployment). No API keys, no test suite.**

## Setup
- Windows, Python 3.14, project in OneDrive. Keep `.venv` and model cache out of git. Empty `screenshots/.gitkeep`.
- Install the **CPU-only PyTorch build** (`pip install torch --index-url https://download.pytorch.org/whl/cpu`) - NOT the CUDA build. Plus `transformers`, `sentence-transformers`, `faiss-cpu`, `flask`, `requests`. Pin `requirements.txt`.
- **Reuse, don't re-download:**
  - Knowledge base + search code: clone my public Task 7 repo `https://github.com/Krishna141414/semantic-search-embeddings` into a temp folder, copy `data/articles.json` and the useful chunking/embedding/search code, then delete the temp clone. Don't modify that repo.
  - LLM: list the Hugging Face cache (`%USERPROFILE%\.cache\huggingface\hub`) and reuse the small instruct model already there (e.g. Qwen2.5-0.5B-Instruct). Embeddings: `all-MiniLM-L6-v2` (also likely cached).

## Pipeline (`rag.py`, short and commented)
1. **Ingestion + cleaning:** load the Wikipedia travel articles, clean text (remove references/extra whitespace/empty sections).
2. **Chunking:** ~500-char chunks with overlap, keep title + chunk id.
3. **Embeddings + vector store:** all-MiniLM-L6-v2 + FAISS index saved to `index/` (build once, load after).
4. **Retrieval:** top-k chunks (k=3) with similarity scores.
5. **Unanswerable handling:** if the best score is below a threshold, return "I couldn't find this in the travel guide documents" without calling the LLM. The prompt also tells the LLM to say it doesn't know if the context lacks the answer.
6. **Prompt construction:** system instruction + numbered context chunks + question; "answer only from the context and cite sources like [1]".
7. **Generation:** local LLM, low temperature, short max_new_tokens.
8. Return: answer, sources (title, chunk text snippet, score), and status (answered / not found).

## Web app (`app.py` Flask + `templates/index.html`, inline CSS/JS)
- One page: question box + Ask button + 4-5 example question chips (including 1-2 unanswerable ones, e.g. "What is the capital of Brazil?").
- Shows: the answer, a status badge (Answered / Not in documents), and expandable **source cards** (article title, score, snippet). A small toggle to show the exact prompt sent to the LLM.
- Loading spinner while generating (CPU can take some seconds).
- Look: dark navy `#0B1020`, gradient header (electric blue `#4F7CFF` -> neon pink `#FF3D81`), marigold `#FFB020` and mint `#22D3B6` accents, rounded cards. Simple, clean, responsive.

## Quick check (`evaluate.py`)
- ~10 questions: 7 answerable (with expected article) + 3 unanswerable. Record: retrieval hit (right article in sources), correct "not found" handling, avg response time. Save `results.md` with a small table.

## README
Problem, knowledge base + Wikipedia credit (CC BY-SA), RAG pipeline diagram (text), how unanswerable questions are handled, results table, limitations (small LLM, CPU speed, 25 articles), how to run (`python app.py`, open localhost).

## Rules
- Do everything in one go without asking. Keep code short and commented.
- Run `evaluate.py` once, start the app and check a couple of questions work, then commit and push.
- Finish with a SHORT summary: results table + how to run. Then stop.


## Web page: follow SHOWCASE.md
- SHOWCASE.md (in this folder) defines the web page. It overrides any web-page details above (keep the same features, presented as SHOWCASE.md describes).
