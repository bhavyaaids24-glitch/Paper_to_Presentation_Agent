from langchain_core.prompts import ChatPromptTemplate
from agents.model import llm

ALLOWED_INTENTS = {"summary", "concepts", "slides", "viva", "chat"}

def detect_intent(user_input: str) -> str:
    """LLM-based intent detection. Defaults safely to chat."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Classify the user's request into exactly one label:
summary, concepts, slides, viva, chat.
- summary: summarize or explain the paper overall
- concepts: extract concepts, contributions, methods, results or limitations
- slides: create a PowerPoint or presentation
- viva: generate or practise viva/examiner questions
- chat: ask a specific question about the paper
Return only the label, with no punctuation or explanation."""),
        ("human", "{request}")
    ])
    try:
        result = (prompt | llm).invoke({"request": user_input})
        label = result.content.strip().lower().split()[0].strip(".,:;")
        return label if label in ALLOWED_INTENTS else "chat"
    except Exception:
        # A simple fallback if the intent-classification API call fails.
        text = user_input.lower()
        if any(word in text for word in ["ppt", "powerpoint", "slide", "presentation"]):
            return "slides"
        if any(word in text for word in ["viva", "examiner", "question"]):
            return "viva"
        if any(word in text for word in ["concept", "method", "contribution", "result"]):
            return "concepts"
        if any(word in text for word in ["summary", "summarize", "summarise"]):
            return "summary"
        return "chat"
