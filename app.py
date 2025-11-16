# app_local.py — SafeRoad AI (Lovable + Premium UI)
# Fully cleaned, no example buttons, no session_state errors.

import os
import io
from pathlib import Path
import re
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="Road Safety Intervention — SafeRoad AI",
    page_icon="🚦",
    layout="wide"
)

# ----- LOVABLE PREMIUM CSS -----
lovable_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Poppins", sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #f3e7ff 0%, #e3f0ff 50%, #fff8f3 100%);
    background-attachment: fixed;
}

/* Hero Section */
.sr-hero {
    background: linear-gradient(90deg, rgba(17,128,214,0.06), rgba(76,195,255,0.03));
    border-radius: 18px;
    padding: 36px;
    margin-bottom: 22px;
    box-shadow: 0 16px 40px rgba(17,128,214,0.06);
    display:flex; 
    align-items:center; 
    gap:20px;
}
.sr-hero h1 { 
    font-size:42px; 
    margin:0; 
    color:#0f172a; 
    font-weight:800; 
    line-height:1; 
}
.sr-hero .lead { 
    color: #334155; 
    font-weight:500; 
    opacity:0.85; 
    margin-top:6px; 
}

/* Features */
.feature-row { 
    display:flex; 
    gap:14px; 
    margin-top:18px; 
}
.feature-tile {
    background: #fff; 
    border-radius:12px; 
    padding:18px; 
    width:100%;
    box-shadow: 0 10px 20px rgba(15,23,42,0.04); 
    border:1px solid rgba(15,23,42,0.03);
}

/* Layout */
.wrap { 
    display:flex; 
    gap:22px; 
    align-items:flex-start; 
    margin-bottom:18px; 
}
.left { 
    flex:0 0 42%; 
    min-width:300px; 
}
.right { 
    flex:1; 
}

/* Cards */
.card {
    background: rgba(255,255,255,0.95); 
    border-radius:16px;
    padding:18px; 
    margin-bottom:18px;
    box-shadow: 0 8px 28px rgba(31,41,55,0.05);
    border: 1px solid rgba(15,23,42,0.04);
    transition: transform .16s ease, box-shadow .16s ease;
}
.card:hover { 
    transform: translateY(-4px); 
    box-shadow: 0 18px 46px rgba(17,128,214,0.10); 
}

.muted { 
    color:#6b7280; 
    font-size:14px; 
    margin-top:6px; 
}

/* Pills */
.pill { 
    display:inline-block; 
    padding:6px 10px; 
    border-radius:999px; 
    background:rgba(17,128,214,0.08); 
    color:#0b3b61; 
    font-weight:600; 
    margin-right:8px; 
    font-size:13px; 
}

/* Intervention item */
.interv {
    border-radius: 14px; 
    padding:18px; 
    background:#fff; 
    margin-bottom:16px;
    box-shadow: 0 8px 24px rgba(12,20,30,0.04); 
    border:1px solid rgba(12,20,30,0.03);
    display:flex; 
    gap:14px; 
    align-items:flex-start;
}
.interv .accent { 
    width:6px; 
    background: linear-gradient(180deg,#1180d6,#4cc3ff); 
    border-radius:6px; 
    height:100%; 
}

/* Footer */
.sr-footer { 
    text-align:center; 
    color:#475569; 
    margin-top:14px; 
    font-size:13px; 
}
</style>
"""
st.markdown(lovable_style, unsafe_allow_html=True)

# ----- Load Interventions CSV -----
INTERVENTIONS_CSV = os.environ.get("INTERVENTIONS_CSV", "data/irc_interventions.csv")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
MODEL_NAME = "models/gemini-2.5-flash"


def load_interventions(csv_path):
    p = Path(csv_path)
    if p.exists():
        try:
            df = pd.read_csv(p)
            if "keywords" not in df.columns:
                df["keywords"] = ""
            return df
        except:
            return pd.DataFrame(columns=["title", "description", "keywords"])
    else:
        return pd.DataFrame([
            {"title": "Pothole Repair", "description": "Patch and re-lay carriageway.", "keywords": "pothole"},
            {"title": "Improved Lighting", "description": "Install LED lighting.", "keywords": "lighting"},
            {"title": "Drainage Clearing", "description": "Clear blocked drains.", "keywords": "drain,flood"},
        ])


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip()
    except:
        return ""


def extract_road_issues(text):
    if not text:
        return []
    pattern = r"(?i)\b(pothole|crack|sign|lighting|barrier|shoulder|accident|drain|flood|curve|school|intersection)\b"
    found = re.findall(pattern, text)
    return list({x.lower() for x in found})


def normalize_keywords(k):
    if isinstance(k, str):
        return [x.strip().lower() for x in k.split(",") if x.strip()]
    return []


def find_matching_interventions(issues, df):
    matches = []
    for _, row in df.iterrows():
        kws = normalize_keywords(row.get("keywords", ""))
        desc = row.get("description", "").lower()
        title = row.get("title", "").lower()

        for iss in issues:
            if iss in kws or iss in desc or iss in title:
                matches.append(row)
                break

    if matches:
        return pd.DataFrame(matches)
    return pd.DataFrame()


def generate_ai_summary(issue_text, result_df):
    short = issue_text[:600]
    df_small = result_df.head(5)
    prompt = f"""
Summarize the road safety issue and suggest top interventions.
Issue: {short}
Interventions: {df_small.to_string(index=False)}
"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        res = model.generate_content(prompt)
        return res.text or "No summary generated."
    except:
        return "AI Summary unavailable."


interventions_df = load_interventions(INTERVENTIONS_CSV)

# ----- HERO -----
st.markdown("""
<div class="sr-hero">
    <div style="flex:1;">
        <h1>SafeRoad AI - Road Safety Intervention<br><span style="color:#1180d6;">Decision Support System</span></h1>
        <div class="lead">AI-powered analysis + IRC/WHO best practices.</div>
        <div style="font-weight:700; color:#08375f;">By Team Ignite</div>
        <div class="feature-row">
            <div class="feature-tile"><b>Smart Analysis</b><div class="muted">AI analyzes your road safety issues against global standards and proven methodologies.</div></div>
            <div class="feature-tile"><b>Evidence-Based</b><div class="muted">Recommendations backed by MUTCD, AASHTO, WHO guidelines, and audit reports.</div></div>
            <div class="feature-tile"><b>Expert Guidance</b><div class="muted">Get prioritized interventions with implementation considerations and references.</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----- MAIN LAYOUT -----
st.markdown("<div class='wrap'>", unsafe_allow_html=True)

# LEFT
st.markdown("<div class='left'>", unsafe_allow_html=True)

# Input Mode
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Get started</h3>", unsafe_allow_html=True)
mode = st.radio("", ("📝 Describe Manually", "📄 Upload PDF Report"))
st.markdown("</div>", unsafe_allow_html=True)

# Manual
user_input = None
uploaded_pdf = None

if mode == "📝 Describe Manually":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Describe the road issue</h3>", unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="Example: High-speed curve with insufficient signage", height=180)
    analyze_manual = st.button("Analyze Issue")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Upload Road Report (PDF)</h3>", unsafe_allow_html=True)
    uploaded_pdf = st.file_uploader("", type=["pdf"])
    st.markdown("</div>", unsafe_allow_html=True)

# Tips Card
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Tips for best results</h3>", unsafe_allow_html=True)
st.markdown("""
<ul class='sr-list'>
<li>Include exact location (km marker, landmark)</li>
<li>Mention day/night & lighting issues</li>
<li>Describe visible damages or traffic behavior</li>
</ul>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close left

# ----- RIGHT (RESULTS) -----
st.markdown("<div class='right'>", unsafe_allow_html=True)

def render_interventions(df):
    for _, row in df.iterrows():
        title = row["title"]
        desc = row["description"]
        priority = row.get("priority", "Medium")
        eff = row.get("effectiveness", "Medium")
        comp = row.get("complexity", "Moderate")

        html = f"""
        <div class='interv'>
            <div class='accent'></div>
            <div class='body'>
                <div style="font-weight:700; font-size:18px; color:#08375f;">{title}</div>
                <div style="margin-top:8px; color:#334155;">{desc}</div>
                <div style="margin-top:10px;">
                    <span class="pill">Priority: {priority}</span>
                    <span class="pill">Effectiveness: {eff}</span>
                    <span class="pill">Complexity: {comp}</span>
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# --- MANUAL MODE ---
if mode == "📝 Describe Manually" and user_input and analyze_manual:
    with st.spinner("Analyzing issue..."):
        issues = extract_road_issues(user_input)
        matches = find_matching_interventions(issues, interventions_df)

    # Results
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Analysis Results</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='muted'>Detected issues: {', '.join(issues)}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Recommended Interventions</h3>", unsafe_allow_html=True)
    if not matches.empty:
        render_interventions(matches)
    else:
        st.warning("No matching interventions found.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>AI Summary</h3>", unsafe_allow_html=True)
    st.write(generate_ai_summary(user_input, matches))
    st.markdown("</div>", unsafe_allow_html=True)

# --- PDF MODE ---
elif mode == "📄 Upload PDF Report" and uploaded_pdf:
    with st.spinner("Extracting and analyzing PDF..."):
        pdf_text = extract_text_from_pdf(io.BytesIO(uploaded_pdf.read()))
        issues = extract_road_issues(pdf_text)
        matches = find_matching_interventions(issues, interventions_df)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Extracted text (preview)</h3>", unsafe_allow_html=True)
    st.text_area("", pdf_text[:2000], height=260)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Recommended Interventions</h3>", unsafe_allow_html=True)
    if not matches.empty:
        render_interventions(matches)
    else:
        st.warning("No matches found in PDF.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>AI Summary</h3>", unsafe_allow_html=True)
    st.write(generate_ai_summary(pdf_text[:2000], matches))
    st.markdown("</div>", unsafe_allow_html=True)

# ---- DEFAULT OVERVIEW ----
else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Quick snapshot of dataset.</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='margin-top:12px;'>
            <div style='background:#fff; padding:12px; border-radius:12px; width:160px; text-align:center;'>
                <strong style='font-size:20px'>{len(interventions_df)}</strong>
                <div class='muted'>Interventions</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close right
st.markdown("</div>", unsafe_allow_html=True)  # close wrap

# ----- FOOTER -----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='sr-footer'>🚦 <b>SafeRoad AI © 2025 | Team Ignite</b> • Built with ❤ using Streamlit</div>", unsafe_allow_html=True)
