from agents.common import run_grounded_agent

def answer_question(question: str, context: str) -> str:
    return run_grounded_agent(
        f"""You are a helpful research-paper assistant.
Answer the user's question directly and simply. Base the answer only on the retrieved passages.
If the passages do not contain enough information, say that the answer is not available in the retrieved parts and suggest checking the relevant section of the PDF.
User question: {question}""",
        context
    )
