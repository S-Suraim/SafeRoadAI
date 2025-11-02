import os
import pandas as pd
import re
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# ========================
# 1️⃣ GEMINI CONFIGURATION
# ========================
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"


# ========================
# 2️⃣ PDF TEXT EXTRACTION
# ========================
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# ========================
# 3️⃣ ISSUE EXTRACTION
# ========================
def extract_road_issues(text):
    pattern = r"(?i)(pothole|crack|sign|marking|lighting|barrier|shoulder|accident|flood|drain|school|curve|visibility|intersection)"
    return list(set(re.findall(pattern, text)))

# ========================
# 4️⃣ MATCH INTERVENTIONS
# ========================
def find_matching_interventions(issues, df):
    matches = []
    for issue in issues:
        for _, row in df.iterrows():
            if isinstance(row["keywords"], str) and any(k.strip().lower() in issue.lower() for k in row["keywords"].split(",")):
                matches.append(row.to_dict())
    return pd.DataFrame(matches).drop_duplicates()

# ========================
# 5️⃣ AI SUMMARY (Gemini)
# ========================
def generate_ai_summary(issue_text, interventions_df):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
You are a road safety engineer. Based on the described issue and interventions below,
generate a professional explanation suitable for a safety improvement report.

Road Issue:
{issue_text}

Matched Interventions:
{interventions_df.to_string(index=False)}
"""
        response = model.generate_content(prompt)
        return response.text if response and response.text else "No summary generated."
    except Exception as e:
        return f"⚠️ AI summary generation failed: {str(e)}"

# ========================
# 6️⃣ STREAMLIT APP UI
# ========================
st.set_page_config(page_title="🚧 SafeRoad AI", page_icon="🚦", layout="wide")
st.title("🚧 SafeRoad AI – Road Safety Intervention GPT")
st.markdown("""
Analyze road safety issues and get AI-powered intervention suggestions with explanations.
Upload a **PDF report** or **enter your issue manually**.
""")

# Load CSV
try:
    df = pd.read_csv("data/irc_interventions.csv")
except FileNotFoundError:
    st.error("❌ 'irc_interventions.csv' not found. Please make sure it's in the same folder as app.py.")
    st.stop()

option = st.radio("Select Input Type:", ["📝 Describe Manually", "📄 Upload PDF Report"])

# ========================
# 7️⃣ MANUAL TEXT INPUT
# ========================
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
                ai_summary = generate_ai_summary(user_input, matched_rows)
                st.write(ai_summary)
            else:
                st.warning("No valid interventions found for this issue.")
        else:
            st.warning("Please describe the road issue first.")

# ========================
# 8️⃣ PDF UPLOAD MODE
# ========================
elif option == "📄 Upload PDF Report":
    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])
    if uploaded_pdf:
        os.makedirs("uploads", exist_ok=True)
        uploaded_pdf_path = os.path.join("uploads", uploaded_pdf.name)

        # Save the uploaded PDF
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
            ai_summary = generate_ai_summary(pdf_text, matched_rows)
            st.write(ai_summary)
        else:
            st.warning("No valid interventions found in the report.")
            
