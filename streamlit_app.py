import ast
import html
import json
import os

import google.generativeai as genai
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)
if api_key:
    genai.configure(api_key=api_key)


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    return "".join(page.extract_text() or "" for page in reader.pages)


PROMPT = """Act as an experienced applicant tracking system for technology roles. Evaluate the resume against the job description and give practical, accurate guidance. Return only a JSON object using this exact schema: {\"JD Match\": \"%\", \"MissingKeywords\": [], \"Profile Summary\": \"\"}.\n\nResume:\n{text}\n\nJob description:\n{jd}"""


def response_data_from(text):
    cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return ast.literal_eval(cleaned)


st.set_page_config(page_title="ResuTrack — Resume analysis", layout="wide", page_icon="✦")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
.stApp{background:radial-gradient(circle at 84% 3%,#25245c 0,transparent 25%),radial-gradient(circle at 0 72%,#164a72 0,transparent 30%),#090b20;color:#eef0ff;font-family:'DM Sans',sans-serif}.block-container{max-width:1120px;padding-top:2.2rem;padding-bottom:4.5rem}.rt-brand{display:flex;align-items:center;gap:10px;color:#fff;font:700 1.05rem 'Plus Jakarta Sans';margin-bottom:2.7rem}.rt-brand span{display:grid;place-items:center;width:30px;aspect-ratio:1;border-radius:10px;background:linear-gradient(135deg,#d4ceff,#8173ff);color:#171237;font-size:.84rem}.rt-eyebrow,.analysis-label{color:#c4c5f5;font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase}.rt-title{font:800 clamp(2.3rem,5vw,4.2rem)/1.06 'Plus Jakarta Sans';letter-spacing:-.075em;margin:.6rem 0 1rem}.rt-title em{font-style:normal;color:#aaa0ff}.rt-subtitle{color:#afb4d5;font-size:1rem;max-width:570px;margin-bottom:2rem}.rt-card,.analysis-card{position:relative;isolation:isolate;background:linear-gradient(145deg,rgba(40,46,102,.7),rgba(20,24,64,.6));border:1px solid rgba(255,255,255,.13);border-radius:18px;padding:1.5rem;box-shadow:0 24px 70px rgba(0,0,28,.28);backdrop-filter:blur(18px);overflow:hidden}.rt-card:before,.analysis-card:before{content:'';position:absolute;inset:0;z-index:-1;border-radius:inherit;background:linear-gradient(115deg,rgba(122,235,255,.12),transparent 28%,rgba(187,143,255,.16) 52%,transparent 72%,rgba(255,161,216,.11));background-size:220% 220%;animation:prism 8s ease-in-out infinite alternate}.rt-card:after,.analysis-card:after{content:'';position:absolute;inset:1px;border-radius:inherit;background:linear-gradient(135deg,rgba(255,255,255,.16),transparent 26%,transparent 75%,rgba(177,245,255,.12));pointer-events:none}h2,h3{font-family:'Plus Jakarta Sans';letter-spacing:-.04em;color:#f0f1ff}.stTextArea textarea,.stFileUploader{background:rgba(5,7,30,.45)!important;border:1px solid rgba(255,255,255,.16)!important;border-radius:10px!important;color:#fff!important}.stTextArea label,.stFileUploader label{color:#dfe1f6!important;font-size:.82rem!important;font-weight:600!important}.stButton>button{width:100%;border:0;border-radius:11px;background:linear-gradient(100deg,#b7adff,#82e0ff);color:#151134;font-weight:700;padding:.8rem;transition:transform .2s,box-shadow .2s}.stButton>button:hover{border:0;color:#151134;transform:translateY(-2px);box-shadow:0 15px 30px #675bc467}.stAlert{border-radius:11px}.analysis-top{display:flex;align-items:center;justify-content:space-between;padding-bottom:1rem;border-bottom:1px solid rgba(255,255,255,.13)}.match-pill{display:inline-block;padding:.35rem .55rem;border-radius:20px;background:#5fdbac1e;color:#a9f9d8;font-size:.72rem;font-weight:700}.analysis-metrics{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:1.2rem 0;border-bottom:1px solid rgba(255,255,255,.13)}.metric-number{display:block;font:700 2.05rem/1 'Plus Jakarta Sans';letter-spacing:-.08em;margin-top:.25rem}.metric-number small{font:400 .73rem 'DM Sans';letter-spacing:0;color:#aeb4d5}.quick-win{display:flex;gap:10px;margin-top:1.2rem;padding:.8rem;border-radius:10px;background:linear-gradient(90deg,#a78bfa23,#63d9ff15);color:#aeb4d5;font-size:.79rem}.quick-win span{color:#b6aaff}.quick-win b{color:#fff}.result-summary{color:#c8cbe3;line-height:1.7;font-size:.9rem;margin-top:.85rem}.stSpinner>div{border-top-color:#9b8dff!important}@keyframes prism{0%{background-position:0% 50%}100%{background-position:100% 50%}}@media(max-width:700px){.block-container{padding:1.4rem 1rem}.rt-title{font-size:2.5rem}}@media(prefers-reduced-motion:reduce){.rt-card:before,.analysis-card:before{animation:none}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="rt-brand"><span>R</span>ResuTrack</div>', unsafe_allow_html=True)
st.markdown('<p class="rt-eyebrow">AI-assisted resume insight</p><h1 class="rt-title">Bring more clarity to<br>your <em>next application.</em></h1><p class="rt-subtitle">Upload your resume and the role you are targeting. We’ll surface the match, missing language, and the strongest next improvement.</p>', unsafe_allow_html=True)

left, right = st.columns([1.25, 1], gap="large")
with left:
    st.markdown('<div class="rt-card">', unsafe_allow_html=True)
    st.subheader("01 · The role")
    jd = st.text_area("Paste the job description", height=250, placeholder="Paste the role description here…")
    st.markdown('</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="rt-card">', unsafe_allow_html=True)
    st.subheader("02 · Your resume")
    uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf", help="PDF files only")
    st.caption("Your document is used only to generate this analysis.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)
submit = st.button("Analyse my resume  →", type="primary", use_container_width=True)

if submit:
    if not uploaded_file or not jd.strip():
        st.error("Add both a job description and a PDF resume to continue.")
    else:
        if not api_key:
            st.error("The analysis service is not configured. Add GOOGLE_API_KEY to Streamlit Community Cloud secrets.")
            st.stop()
        with st.spinner("Reading the match…"):
            resume_text = input_pdf_text(uploaded_file)
            response = genai.GenerativeModel("gemini-pro").generate_content(PROMPT.format(text=resume_text, jd=jd)).text
        try:
            result = response_data_from(response)
            keywords = result.get("MissingKeywords", []) or []
            keyword_count = len(keywords)
            preview_keywords = ", ".join(map(str, keywords[:3])) or "No priority phrases found"
            st.success("Your analysis is ready.")
            st.markdown("### Your analysis, at a glance")
            st.markdown(f'''<div class="analysis-card"><div class="analysis-top"><div><span class="analysis-label">APPLICATION READINESS</span><h3 style="margin:.25rem 0 0">A strong starting point</h3></div><span class="match-pill">{html.escape(str(result.get("JD Match", "N/A")))} match</span></div><div class="analysis-metrics"><div><span class="analysis-label">RESUME STATUS</span><strong class="metric-number">Ready <small>PDF analysed</small></strong></div><div><span class="analysis-label">TO ADD</span><strong class="metric-number">{keyword_count} <small>key phrases</small></strong></div></div><div class="quick-win"><span>✦</span><p><b>Quick win</b><br>Add {html.escape(preview_keywords)} to strengthen your keyword coverage.</p></div></div>''', unsafe_allow_html=True)
            st.markdown("#### Profile summary")
            st.markdown(f'<div class="rt-card result-summary">{html.escape(str(result.get("Profile Summary", "No summary provided.")))}</div>', unsafe_allow_html=True)
            if keywords:
                st.markdown("#### Keywords to consider")
                st.write(" · ".join(map(str, keywords)))
        except (ValueError, SyntaxError, TypeError):
            st.error("We received an unexpected response format. Please try again.")
