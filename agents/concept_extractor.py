from agents.common import run_grounded_agent

def extract_concepts(context: str) -> str:
    return run_grounded_agent(
        """You are a research concept-extraction agent.
Extract and explain:
1. Main research problem
2. Key concepts and terminology
3. Main contributions
4. Technologies, algorithms or models used
5. Research methodology
6. Important findings/results
7. Limitations and future scope
Use bullet points and simple language. Do not add concepts that are not supported by the context.""",
        context
    )
