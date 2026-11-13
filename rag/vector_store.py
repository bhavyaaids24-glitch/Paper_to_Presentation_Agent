from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

_embedding_model = None

def get_embeddings():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embedding_model

def create_vector_store(chunks):
    # A fresh in-memory collection avoids mixing one upload with another.
    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name="research_paper_session",
    )
