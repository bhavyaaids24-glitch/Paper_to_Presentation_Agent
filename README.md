# Paper-to-Presentation & Viva Agent

## Requirements
- Python 3.10+
- A Groq API key
- Internet connection for Groq API and the first download of the local embedding model

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Open `.env` and add your Groq API key. Never share or commit this file.

## Run
```powershell
streamlit run app.py
```

## Features
- PDF text extraction with PyPDF
- Text chunking
- Local Hugging Face embeddings
- ChromaDB similarity retrieval
- Groq-powered summarizer, concept extractor, slide generator and viva agent
- LLM intent routing
- Research-paper Q&A
- Downloadable PowerPoint

## Notes
- This starter version works with text-based PDFs. Scanned/image-only PDFs need OCR, which is not included.
- The default Groq model is configured in `.env` as `llama-3.3-70b-versatile`. If Groq no longer lists that model, change `GROQ_MODEL` to a currently available chat model in your Groq console.
- The app creates a new in-session vector store each time a PDF is processed. It does not permanently save uploaded papers.
- Verify generated content against the original research paper before presenting or submitting it.
