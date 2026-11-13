from agents.common import run_grounded_agent

def generate_viva(context: str, difficulty: str = "Mixed", count: int = 10) -> str:
    return run_grounded_agent(
        f"""You are a university examiner preparing a viva.
Generate exactly {count} questions at {difficulty} difficulty.
For each question, provide:
- Question
- Model answer in clear, simple language
- What the examiner is testing
Cover the research problem, objectives, definitions, methodology, design choices, results, limitations and future work where supported.
Do not ask about details absent from the context without clearly marking them as questions the student should verify in the full paper.""",
        context
    )
