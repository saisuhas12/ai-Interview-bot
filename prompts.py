# prompts.py
GEN_QUESTIONS_PROMPT = """
You are an expert interview coach. Given the job description below, generate {num_q} interview questions tailored to the role.
- Include behavioral questions: {include_behavioral}
- Include technical questions: {include_technical}

Return a numbered list (1. Question ...).
Job description:
{jd}
"""

GEN_ANSWER_PROMPT = """
You are an expert interview coach. For the question below, produce a concise, high-quality sample answer tailored to the job description.
Return the answer as plain text.

Job description:
{jd}

Question:
{question}
"""

EVAL_PROMPT = """
You are an objective interview evaluator. Evaluate the following user answer to a given interview question with respect to the job description.
Return ONLY valid JSON with these fields:
- score: integer 1-10
- category_scores: object with keys "content","structure","relevance","clarity" (each 1-10)
- feedback: short paragraph with actionable feedback
- improved_answer: a revised, stronger answer

Job description:
{jd}

Question:
{question}

User answer:
{user_answer}

Return JSON only.
"""
