import os
import tempfile
import streamlit as st

from rag.pdf_loader import process_pdf
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_context
from agents.router import detect_intent
from agents.summarizer import summarize
from agents.concept_extractor import extract_concepts
from agents.slide_generator import generate_slides
from agents.viva_agent import generate_viva
from agents.chat_agent import answer_question
from utils.ppt_generator import create_ppt

st.set_page_config(page_title="Paper-to-Presentation & Viva Agent", page_icon="📚", layout="wide")

st.title("📚 Paper-to-Presentation & Viva Agent")
st.caption("Upload a research paper to create a grounded summary, extract concepts, generate slides, and prepare for viva.")

with st.sidebar:
    st.header("About")
    st.write("This app uses Groq for language generation, local Hugging Face embeddings, and ChromaDB for retrieval.")
    st.info("Answers are generated from the uploaded paper where possible. Always verify important academic claims against the original PDF.")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type=["pdf"])

if uploaded_file is not None:
    if st.button("Process research paper", type="primary"):
        try:
            with st.spinner("Extracting text and building the searchable paper index..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    temp_path = tmp.name
                try:
                    chunks, page_count = process_pdf(temp_path)
                    if not chunks:
                        st.error("No readable text was found. This may be a scanned PDF; OCR is not included in this version.")
                        st.stop()
                    db = create_vector_store(chunks)
                    st.session_state["vector_db"] = db
                    st.session_state["paper_name"] = uploaded_file.name
                    st.session_state["processed"] = True
                    st.session_state["chat_history"] = []
                    st.success(f"Processed {uploaded_file.name}: {page_count} pages, {len(chunks)} text chunks.")
                finally:
                    os.unlink(temp_path)
        except Exception as exc:
            st.error(f"Could not process the PDF: {exc}")

if st.session_state.get("processed"):
    st.success(f"Ready: {st.session_state.get('paper_name', 'Research paper')}")
    st.divider()

    tab_summary, tab_concepts, tab_slides, tab_viva, tab_chat = st.tabs(
        ["Summary", "Concepts", "PowerPoint", "Viva Practice", "Ask the Paper"]
    )

    def run_agent(label, fn, query):
        try:
            with st.spinner(f"{label} is working..."):
                context, sources = retrieve_context(st.session_state["vector_db"], query)
                result = fn(context)
            st.markdown(result)
            with st.expander("Retrieved source passages"):
                for source in sources:
                    st.caption(f"Page {source['page']}")
                    st.write(source["text"])
            return result
        except Exception as exc:
            st.error(f"{label} failed: {exc}")
            return None

    with tab_summary:
        st.subheader("Research paper summary")
        if st.button("Generate summary", key="summary_btn"):
            run_agent("Summarizer Agent", summarize,
                      "Find the paper's title, abstract, research problem, objectives, methodology, results, limitations and conclusion.")

    with tab_concepts:
        st.subheader("Important concepts and contributions")
        if st.button("Extract concepts", key="concept_btn"):
            run_agent("Concept Extractor Agent", extract_concepts,
                      "Find the main research contributions, important concepts, technologies, methodology, findings and limitations.")

    with tab_slides:
        st.subheader("Presentation generator")
        st.write("Create a concise 9-slide academic presentation.")
        if st.button("Generate slide content", key="slides_btn"):
            result = run_agent("Slide Generator Agent", generate_slides,
                               "Retrieve information needed for a 9-slide presentation: title, background, problem, objectives, methodology, system or approach, results, conclusion and future work.")
            if result:
                st.session_state["slide_content"] = result
        if st.session_state.get("slide_content"):
            if st.button("Build PowerPoint file", key="ppt_btn"):
                try:
                    ppt_bytes = create_ppt(st.session_state["slide_content"], st.session_state.get("paper_name", "Research Paper"))
                    st.download_button(
                        "Download PowerPoint",
                        data=ppt_bytes,
                        file_name="Research_Presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
                except Exception as exc:
                    st.error(f"PowerPoint generation failed: {exc}")

    with tab_viva:
        st.subheader("Viva preparation")
        difficulty = st.selectbox("Question difficulty", ["Mixed", "Basic", "Intermediate", "Advanced"])
        count = st.slider("Number of questions", min_value=5, max_value=20, value=10)
        if st.button("Generate viva questions", key="viva_btn"):
            query = f"Retrieve key definitions, objectives, methods, experiments, findings and limitations for {difficulty} viva questions."
            try:
                with st.spinner("Viva Agent is preparing questions..."):
                    context, sources = retrieve_context(st.session_state["vector_db"], query)
                    result = generate_viva(context, difficulty, count)
                st.markdown(result)
                with st.expander("Retrieved source passages"):
                    for source in sources:
                        st.caption(f"Page {source['page']}")
                        st.write(source["text"])
            except Exception as exc:
                st.error(f"Viva generation failed: {exc}")

    with tab_chat:
        st.subheader("Ask questions about your paper")
        for item in st.session_state.get("chat_history", []):
            with st.chat_message(item["role"]):
                st.markdown(item["content"])
        question = st.chat_input("Ask about the research paper...")
        if question:
            st.session_state["chat_history"].append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                try:
                    with st.spinner("Searching the paper..."):
                        context, sources = retrieve_context(st.session_state["vector_db"], question)
                        answer = answer_question(question, context)
                    st.markdown(answer)
                    with st.expander("Sources used"):
                        for source in sources:
                            st.caption(f"Page {source['page']}")
                            st.write(source["text"])
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                except Exception as exc:
                    st.error(f"Could not answer: {exc}")

else:
    st.info("Upload a PDF and click **Process research paper** to get started.")
    st.markdown("""
    **What this application can do**
    - Summarize the uploaded research paper.
    - Extract concepts, methods, contributions and findings.
    - Generate a PowerPoint presentation.
    - Prepare viva questions with model answers.
    - Answer questions using retrieved passages from the paper.
    """)
