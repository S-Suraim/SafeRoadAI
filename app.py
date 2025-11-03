import os
import pandas as pd
import re
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import textwrap

# =========================================================
# 1️⃣ GEMINI CONFIGURATION — Safe for Local & Streamlit
# =========================================================
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ Google API Key not found.")
    st.stop()

genai.configure(api_key=API_KEY)

# Try to load a valid model
try:
    available_models = [m.name for m in genai.list_models()]
    MODEL_NAME = next((m for m in available_models if "gemini" in m.lower()), "models/gemini-pro")
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.warning(f"⚠️ Falling back to gemini-pro due to: {e}")
    model = genai.GenerativeModel("models/gemini-pro")

# =========================================================
# 2️⃣ PDF TEXT EXTRACTION
# =========================================================
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# =========================================================
# 3️⃣ ISSUE EXTRACTION
# =========================================================
def extract_road_issues(text):
    pattern = r"(?i)(pothole|crack|sign|marking|lighting|barrier|shoulder|accident|flood|drain|school|curve|visibility|intersection)"
    return list(set(re.findall(pattern, text)))

# =========================================================
# 4️⃣ MATCH INTERVENTIONS
# =========================================================
def find_matching_interventions(issues, df):
    matches = []
    for issue in issues:
        for _, row in df.iterrows():
            if isinstance(row["keywords"], str) and any(k.strip().lower() in issue.lower() for k in row["keywords"].split(",")):
                matches.append(row.to_dict())
    return pd.DataFrame(matches).drop_duplicates()

# =========================================================
# 5️⃣ OPTIMIZED AI SUMMARY (Manual Trigger + Fast)
# =========================================================
def generate_ai_summary(text):
    try:
        short_text = text[:1500]
        prompt = f"""
        Summarize the following road safety report in 5 bullet points.
        Focus on detected issues, suggested improvements, and key safety actions.
        Text:
        {short_text}
        """
        response = model.generate_content(prompt)
        return textwrap.fill(response.text.strip(), width=100)
    except Exception as e:
        return f"⚠️ AI summary generation failed: {e}"

# =========================================================
# 6️⃣ STREAMLIT APP UI
# =========================================================
st.set_page_config(page_title="🚧 SafeRoad AI", page_icon="🚦", layout="wide")
st.title("🚧 SafeRoad AI – Road Safety Intervention GPT")

st.markdown("""
Analyze road safety issues and get **AI-powered IRC-based intervention suggestions**.  
Upload a **PDF report** or **enter your issue manually**.
""")

# =========================================================
# 7️⃣ LOAD DATA
# =========================================================
try:
    df = pd.read_csv("data/irc_interventions.csv")
except FileNotFoundError:
    st.error("❌ 'irc_interventions.csv' not found. Make sure it's in the `data/` folder.")
    st.stop()

# =========================================================
# 8️⃣ INPUT OPTION
# =========================================================
option = st.radio("Select Input Type:", ["📝 Describe Manually", "📄 Upload PDF Report"])

# ---------------------------------------------------------
# Manual Input
# ---------------------------------------------------------
if option == "📝 Describe Manually":
    user_input = st.text_area("Describe the road safety issue:", height=150)

    if st.button("🔍 Analyze Issue"):
        if user_input.strip():
            issues = extract_road_issues(user_input)
            matched_rows = find_matching_interventions(issues, df)

            if not matched_rows.empty:
                st.subheader("✅ Recommended Road Safety Interventions")
                st.dataframe(matched_rows)

                st.subheader("💡 AI Summary and Explanation")
                if st.button("🧠 Generate AI Summary"):
                    with st.spinner("Generating AI summary... Please wait"):
                        ai_summary = generate_ai_summary(user_input)
                    st.success("✅ AI Summary Generated Successfully")
                    st.text_area("AI Summary Output", ai_summary, height=250)
                else:
                    st.info("Click '🧠 Generate AI Summary' to generate AI explanation.")
            else:
                st.warning("No valid interventions found for this issue.")
        else:
            st.warning("Please describe the road issue first.")

# ---------------------------------------------------------
# PDF Upload
# ---------------------------------------------------------
elif option == "📄 Upload PDF Report":
    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_pdf:
        os.makedirs("uploads", exist_ok=True)
        uploaded_pdf_path = os.path.join("uploads", uploaded_pdf.name)

        with open(uploaded_pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        st.success("✅ PDF uploaded successfully!")

        pdf_text = extract_text_from_pdf(uploaded_pdf_path)
        st.text_area("📜 Extracted Text (Preview)", pdf_text[:1500], height=200)

        issues = extract_road_issues(pdf_text)
        matched_rows = find_matching_interventions(issues, df)

        if not matched_rows.empty:
            st.subheader("✅ Recommended Interventions from Report")
            st.dataframe(matched_rows)

            st.subheader("💡 AI Summary and Explanation")
            if st.button("🧠 Generate AI Summary"):
                with st.spinner("Generating AI summary... Please wait"):
                    ai_summary = generate_ai_summary(pdf_text)
                st.success("✅ AI Summary Generated Successfully")
                st.text_area("AI Summary Output", ai_summary, height=250)
            else:
                st.info("Click '🧠 Generate AI Summary' to generate AI explanation.")
        else:
            st.warning("No valid interventions found in the report.")
