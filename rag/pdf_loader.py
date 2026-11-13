from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Ignore blank pages but preserve page metadata for source display.
    pages = [page for page in pages if page.page_content and page.page_content.strip()]
    if not pages:
        return [], 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=180,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(pages)
    return chunks, len(pages)
