# app.py
import os, json, re
import streamlit as st
from dotenv import load_dotenv
from prompts import GEN_QUESTIONS_PROMPT, GEN_ANSWER_PROMPT, EVAL_PROMPT
from utils import extract_text_from_file, extract_json

# ---- Load environment variables ----
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-1.5-flash")
if not GEMINI_API_KEY:
    st.error("Missing GEMINI_API_KEY. Add it to .env and restart.")
    st.stop()

# Gemini client
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(GEMINI_MODEL_ID)

def _generate_text(prompt, *, max_new_tokens=512, temperature=0.7):
    """Call Gemini API and return generated text."""
    try:
        resp = gemini_model.generate_content(
            prompt,
            generation_config={
                "temperature": float(temperature),
                "max_output_tokens": int(max_new_tokens),
                "top_p": 0.9,
            },
        )
        text = (resp.text or "").strip()
        return text
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}")

st.set_page_config(page_title="AI Interview Q&A Bot", page_icon="🎯", layout="wide")

# ---- Minimal custom styling ----
st.markdown(
    """
    <style>
    .big-title { font-size: 2rem; font-weight: 800; margin-bottom: .25rem; }
    .subtext { color: #6b7280; margin-bottom: 1rem; }
    .section-card { padding: 1rem 1.25rem; border: 1px solid #e5e7eb; border-radius: 10px; background: #ffffffaa; }
    .stButton>button { border-radius: 8px; height: 3rem; font-weight: 600; }
    .stDownloadButton>button { border-radius: 8px; }
    .muted { color: #6b7280; font-size: .9rem; }
    .count-badge { display:inline-block; padding: .15rem .6rem; border-radius: 999px; background:#eef2ff; color:#4338ca; font-weight:700; margin-left:.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='big-title'>AI Interview Q&A Bot</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtext'>Paste a job description or upload a file, then generate interview questions, sample answers, and get feedback on your own answers.</div>",
    unsafe_allow_html=True,
)

# ---- Sidebar controls ----
with st.sidebar:
    st.markdown("### Settings")
    uploaded_file = st.file_uploader("Upload JD (PDF/DOCX/TXT)", type=['pdf','docx','txt'])
    num_q = st.slider("Number of questions", min_value=3, max_value=20, value=8)
    include_behavioral = st.checkbox("Include behavioral/HR questions", value=True)
    include_technical = st.checkbox("Include technical questions", value=True)
    sidebar_generate = st.button("Generate questions and sample answers", use_container_width=True)

# ---- Input area (main) ----
jd = st.text_area("Paste job description", height=260, placeholder="Paste job description here...")

with st.expander("Tips for best results", expanded=False):
    st.markdown("- Add key responsibilities, required skills, and preferred qualifications.\n- Remove unrelated boilerplate to speed up generation.\n- 5–15 bullet points is usually enough.")

if uploaded_file:
    extracted = extract_text_from_file(uploaded_file)
    if extracted:
        jd = (jd + "\n\n" + extracted).strip()
    else:
        st.info("Uploaded file couldn't be fully parsed; consider copy/pasting the JD.")

st.caption(f"JD length: {len(jd)} characters")

# ---- Generate Questions & Answers ----
main_generate = st.button("Generate questions and sample answers", use_container_width=True)
generate_clicked = sidebar_generate or main_generate

if generate_clicked:
    if not jd or jd.strip() == "":
        st.error("Please paste or upload a job description first.")
    else:
        @st.cache_data(show_spinner=False)
        def _gen_questions_cached(jd_val, num_q_val, include_behavioral_val, include_technical_val):
            prompt_q_local = GEN_QUESTIONS_PROMPT.format(
                jd=jd_val, num_q=num_q_val,
                include_behavioral=str(include_behavioral_val),
                include_technical=str(include_technical_val)
            )
            return _generate_text(prompt_q_local, max_new_tokens=512, temperature=0.7)

        with st.spinner("Generating questions..."):
            try:
                questions_text = _gen_questions_cached(jd, num_q, include_behavioral, include_technical)
            except Exception as e:
                st.error(f"API error generating questions: {e}")
                st.stop()

        st.subheader("Generated Questions")
        st.markdown(questions_text)

        # parse into list
        q_lines = []
        for line in questions_text.splitlines():
            line = line.strip()
            if not line:
                continue
            line = re.sub(r'^\d+[\).\s-]*', '', line)
            q_lines.append(line)
        st.session_state['questions'] = q_lines
        st.success(f"Generated {len(q_lines)} questions")

        # 2) generate sample answers (cached + parallel)
        st.subheader("Sample Answers")

        @st.cache_data(show_spinner=False)
        def _gen_answer_cached(jd_val, question_val):
            prompt_a_local = GEN_ANSWER_PROMPT.format(jd=jd_val, question=question_val)
            return _generate_text(prompt_a_local, max_new_tokens=384, temperature=0.7)

        from concurrent.futures import ThreadPoolExecutor, as_completed

        selected_questions = q_lines[:num_q]
        results = [None] * len(selected_questions)
        max_workers = min(4, len(selected_questions) or 1)
        with st.spinner("Generating sample answers..."):
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                futures = {ex.submit(_gen_answer_cached, jd, q): (i, q)
                           for i, q in enumerate(selected_questions, start=1)}
                for fut in as_completed(futures):
                    i, q = futures[fut]
                    try:
                        ans_text = fut.result()
                    except Exception as e:
                        ans_text = f"[Error generating answer: {e}]"
                    results[i-1] = {"question": q, "sample_answer": ans_text}

        for i, item in enumerate(results, start=1):
            st.markdown(f"**Q{i}. {item['question']}**")
            st.write(item['sample_answer'])

        st.session_state['qa_pairs'] = results

# ---- Evaluate user's own answer ----
st.markdown("---")
st.subheader("Evaluate your answer (optional)")

question_to_eval = st.selectbox(
    "Pick a question to answer/evaluate",
    options=st.session_state.get('questions', ["Paste a JD and generate questions first."])
)
user_answer = st.text_area("Type your answer here", height=160)

if st.button("Evaluate my answer"):
    if not jd:
        st.error("Paste a JD first.")
    elif not question_to_eval or question_to_eval.startswith("Paste a JD"):
        st.error("Generate questions first.")
    elif not user_answer.strip():
        st.error("Please type your answer.")
    else:
        with st.spinner("Scoring your answer..."):
            eval_prompt = EVAL_PROMPT.format(jd=jd, question=question_to_eval, user_answer=user_answer)
            try:
                eval_text = _generate_text(eval_prompt, max_new_tokens=256, temperature=0.2)
                parsed = extract_json(eval_text)
                if not parsed:
                    st.warning("Couldn't parse model output as JSON — showing raw content below.")
                    st.code(eval_text)
                else:
                    st.json(parsed)
            except Exception as e:
                st.error(f"Evaluation API error: {e}")

# ---- Download QA pairs ----
if st.session_state.get('qa_pairs'):
    st.markdown("---")
    st.download_button(
        "Download QA pairs as JSON",
        data=json.dumps(st.session_state['qa_pairs'], ensure_ascii=False, indent=2),
        file_name="qa_pairs.json"
    )
