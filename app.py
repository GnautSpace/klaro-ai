import streamlit as st
import os
from pypdf import PdfReader

st.set_page_config(page_title="Klaro - Jargon Simplifier", page_icon="💡", layout="centered")

st.title("Klaro AI")
st.subheader("Turn confusing legal, medical, or official documents into clear, friendly native language.")

st.sidebar.header("Settings")
mode=st.sidebar.selectbox("Choose Document Type:", ["Legal Contract", "Medical Prescription", "Government Bill / Notice"])
target_language=st.sidebar.selectbox("Translate to Language:", ["English", "Spanish", "Hindi", "French", "German"])
enable_voice=st.sidebar.checkbox("Generate Audio (ElevenLabs)", value=False)

uploaded_file=st.file_uploader("Upload your document (PDF or Text)", type=["pdf", "txt"])

if uploaded_file is not None:
    text=""
    if uploaded_file.type=="application/pdf":
        reader=PdfReader(uploaded_file)
        for page in reader.pages:
            text+=page.extract_text()
    else:
        text=uploaded_file.read().decode("utf-8")

    st.write("---")
    st.write("### Document Preview")
    st.text_area("Extracted Text:", text[:1000] + ("..." if len(text) > 1000 else ""), height=150)

    if st.button("Simplify Document"):
        with st.spinner("Klaro is analyzing and simplifying..."):
            simplified_output = f"Simulated Simplification for a {mode} in {target_language}: \n\n1. What this means: Your document is safe, but watch out for clause 4.\n2. What you need to do: Sign only page 3."
            
            st.success("Done!")
            st.write("### Klaro Explanation")
            st.write(simplified_output)
            
            if enable_voice:
                st.info("ElevenLabs audio generation triggered (Connect your API key here).")
