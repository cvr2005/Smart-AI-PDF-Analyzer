# pdf_analyzer_styled.py

import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# -------------------------------
# Set Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Smart PDF Analyzer (Gemini)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------
# Custom CSS for styling
# -------------------------------
st.markdown("""
<style>
/* Background gradient */
body {
    background: linear-gradient(to right, #f5f7fa, #c3cfe2);
}

/* Header styling */
h1 {
    color: #2b2d42;
    text-align: center;
}

/* Text area styling */
textarea {
    background-color: #edf2f4;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

/* Button styling */
.stButton>button {
    background-color: #8d99ae;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 8px 16px;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #ef233c;
    color: white;
}

/* Info / success box styling */
.stInfo, .stSuccess {
    border-radius: 10px;
    padding: 15px;
    background-color: #edf2f4 !important;
    color: #2b2d42;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar: Instructions
# -------------------------------
st.sidebar.title("📘 Smart AI PDF Analyzer")
st.sidebar.markdown("""
Welcome! This tool allows you to:
- Upload PDF files
- Preview content
- Ask questions about the PDF
- Get AI-generated answers using **Gemini 2.5 Pro**
""")
st.sidebar.markdown("---")

# -------------------------------
# Gemini API Setup
# -------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key="AIzaSyA-ShdHuK0x0b5CH5Qry2VTENx0PevaS8U")

# -------------------------------
# Main Page Header
# -------------------------------
st.markdown("<h1>📄 Smart AI PDF Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Upload your PDF and get instant AI insights!</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# File Upload Section
# -------------------------------
uploaded_file = st.file_uploader("📄 Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from PDF... ⏳"):
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    # -------------------------------
    # Display Preview in Two Columns
    # -------------------------------
    st.subheader("📑 Extracted Text Preview")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.text_area("Preview", text[:4000], height=300)

    with col2:
        st.info("💡 Tip: Ask a question below to get AI analysis of the PDF content.")

    # -------------------------------
    # Ask a Question
    # -------------------------------
    st.subheader("💬 Ask a Question")
    user_question = st.text_input("Enter your question:")

    if st.button("🔍 Analyze with Gemini AI") and user_question:
        with st.spinner("Analyzing your PDF with Gemini... ⏳"):
            try:
                model = genai.GenerativeModel("models/gemini-2.5-pro")
                prompt = f"""
                You are a smart PDF content analyzer.
                The following is the content of a PDF document:
                {text[:8000]}

                The user wants to know:
                {user_question}

                Provide a clear, concise, and accurate answer.
                """
                response = model.generate_content(prompt)

                st.success("✅ Analysis Complete!")
                st.markdown("""
                <div style="background-color:#ffd6a5; border-radius:10px; padding:15px; font-weight:500;">
                <strong>AI Answer:</strong><br>
                """ + response.text + "</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

else:
    st.warning("👆 Please upload a PDF file to begin.")
