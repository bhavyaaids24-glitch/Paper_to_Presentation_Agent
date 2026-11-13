from agents.common import run_grounded_agent

def generate_slides(context: str) -> str:
    return run_grounded_agent(
        """You are an academic presentation designer.
Create exactly 9 slides. Format each slide with a heading beginning with '## '.
Under each heading, provide 3-5 concise bullet points beginning with '- '.
Use this structure:
1. Title
2. Introduction / Background
3. Problem Statement
4. Objectives
5. Literature or Research Context (only if present; otherwise key background)
6. Methodology / Proposed Approach
7. Results and Discussion
8. Conclusion
9. Limitations and Future Scope
Keep slide text concise and presentation-ready. Never fabricate experimental results. If results are absent from the supplied context, say so.""",
        context
    )
