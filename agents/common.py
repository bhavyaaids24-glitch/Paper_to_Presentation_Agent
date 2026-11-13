from langchain_core.prompts import ChatPromptTemplate
from agents.model import llm

def run_grounded_agent(system_prompt: str, context: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt + "\n\nUse ONLY the supplied research-paper context. If information is missing, clearly say it is not stated in the provided passages. Do not invent results, citations, authors, or statistics."),
        ("human", "Research-paper context:\n{context}")
    ])
    chain = prompt | llm
    response = chain.invoke({"context": context})
    return response.content if isinstance(response.content, str) else str(response.content)
