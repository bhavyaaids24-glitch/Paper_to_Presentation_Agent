def retrieve_context(vector_db, query: str, k: int = 5):
    docs = vector_db.similarity_search(query, k=k)
    passages = []
    sources = []
    for doc in docs:
        page_number = doc.metadata.get("page")
        page_label = str(page_number + 1) if isinstance(page_number, int) else "Unknown"
        passages.append(f"[Source: PDF page {page_label}]\n{doc.page_content}")
        sources.append({"page": page_label, "text": doc.page_content})
    return "\n\n---\n\n".join(passages), sources
