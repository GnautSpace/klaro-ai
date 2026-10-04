import streamlit as st
import os
import tempfile
import pathlib
from PIL import Image
from google import genai
from gtts import gTTS

st.set_page_config(
    page_title="Klaro - Jargon Simplifier", 
    page_icon=":material/lightbulb:", 
    layout="centered"
)

st.markdown("""
    <style>
    /* Gradient text styling for main title and all markdown headers */
    h1, h3, h4 {
        background: linear-gradient(90deg, #4F46E5 0%, #9333EA 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    h1 {
        text-align: center;
    }
    
    /* Gradient buttons with smooth hover animations */
    .stButton>button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(126, 34, 206, 0.4);
        background: linear-gradient(135deg, #4338CA 0%, #6D28D9 100%);
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stExpander) {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

if 'language' not in st.session_state:
    st.session_state.language = None
if 'ui_texts' not in st.session_state:
    st.session_state.ui_texts = {}

st.sidebar.markdown("### Configuration")
custom_api_key = st.sidebar.text_input(
    "Custom API Key (Optional)", 
    type="password", 
    help="Enter your own Google GenAI key if you want to use your personal quota."
)

backend_api_key = ""
try:
    backend_api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

if not backend_api_key:
    backend_api_key = os.environ.get("GEMINI_API_KEY", "")

api_key = custom_api_key if custom_api_key else backend_api_key

if st.session_state.language is None:
    st.markdown("# :material/lightbulb: Klaro AI")
    st.markdown("<h3 style='text-align: center; color: #6B7280; font-size: 1.1rem; margin-top: -10px;'>Choose your language / Elige tu idioma / Scegli la lingua</h3>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("English"):
            st.session_state.language = "English"
            st.rerun()
    with col2:
        if st.button("Español"):
            st.session_state.language = "Spanish"
            st.rerun()
    with col3:
        if st.button("Italiano"):
            st.session_state.language = "Italian"
            st.rerun()
    with col4:
        if st.button("Français"):
            st.session_state.language = "French"
            st.rerun()
    with col5:
        if st.button("Deutsch"):
            st.session_state.language = "German"
            st.rerun()
        
    st.write("---")
    with st.container(border=True):
        st.markdown("#### Custom Language")
        custom_lang = st.text_input("Or type any other language (e.g., Portuguese, Arabic, Japanese):", placeholder="Type language name...")
        if st.button("Set Language") and custom_lang:
            st.session_state.language = custom_lang
            st.rerun()
    st.stop()

def fetch_ui_via_gemma(lang, key):
    if lang == "English":
        return {
            "title": "Klaro AI",
            "subtitle": "Turn confusing legal, medical, or official documents into clear, friendly native language.",
            "mode_select": "Choose Document Type:",
            "modes": ["Legal Contract", "Medical Prescription", "Government Bill / Notice"],
            "upload": "Upload document photo, scan, or PDF",
            "button": "Simplify Document",
            "spinner": "Klaro and Gemma are analyzing your document...",
            "change_lang": "Change Language"
        }
    
    if lang in st.session_state.ui_texts:
        return st.session_state.ui_texts[lang]
        
    if not key:
        return {
            "title": f"Klaro AI ({lang})",
            "subtitle": "No API key configured. Please add GEMINI_API_KEY to secrets/environment variables or enter a custom key in the sidebar.",
            "mode_select": "Choose Document Type:",
            "modes": ["Legal Contract", "Medical Prescription", "Government Bill / Notice"],
            "upload": "Upload document photo, scan, or PDF",
            "button": "Simplify Document",
            "spinner": "Analyzing...",
            "change_lang": "Change Language"
        }
        
    try:
        client = genai.Client(api_key=key)
        prompt = f"""
        Translate these English UI labels into {lang}. Return them separated by `|` pipe characters in this exact order:
        1. Title (e.g. Klaro AI - Document Simplifier)
        2. Subtitle (e.g. Turn confusing documents into clear, friendly native language.)
        3. ModeSelect (e.g. Choose Document Type:)
        4. Mode1 (e.g. Legal Contract)
        5. Mode2 (e.g. Medical Prescription)
        6. Mode3 (e.g. Government Bill / Notice)
        7. Upload (e.g. Upload document photo, scan, or PDF)
        8. Button (e.g. Simplify Document)
        9. Spinner (e.g. Klaro and Gemma are analyzing your document...)
        10. ChangeLang (e.g. Change Language)
        
        Output ONLY the `|` separated values, nothing else. No markdown formatting.
        """
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=prompt
        )
        parts = [p.strip() for p in response.text.split("|")]
        if len(parts) >= 10:
            ui_dict = {
                "title": parts[0],
                "subtitle": parts[1],
                "mode_select": parts[2],
                "modes": [parts[3], parts[4], parts[5]],
                "upload": parts[6],
                "button": parts[7],
                "spinner": parts[8],
                "change_lang": parts[9]
            }
            st.session_state.ui_texts[lang] = ui_dict
            return ui_dict
    except Exception:
        pass 
        
    return {
        "title": f"Klaro AI ({lang})",
        "subtitle": f"Dynamic UI translation loaded for {lang}.",
        "mode_select": "Choose Document Type:",
        "modes": ["Legal Contract", "Medical Prescription", "Government Bill / Notice"],
        "upload": "Upload document photo, scan, or PDF",
        "button": "Simplify Document",
        "spinner": "Analyzing...",
        "change_lang": "Change Language"
    }

t = fetch_ui_via_gemma(st.session_state.language, api_key)

st.sidebar.markdown("### Language")
st.sidebar.info(f"Active: **{st.session_state.language}**")
if st.sidebar.button(t["change_lang"]):
    st.session_state.language = None
    st.rerun()

st.markdown(f"# :material/lightbulb: {t['title']}")
st.markdown(f"<p style='text-align: center; color: #4B5563; font-size: 1.1rem; margin-bottom: 2rem;'>{t['subtitle']}</p>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.markdown("### Preferences")
    mode = st.selectbox(t["mode_select"], t["modes"])
    enable_voice = st.checkbox("Generate Audio (Native Accent)", value=True)

uploaded_file = st.file_uploader(t["upload"], type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.write("---")
    with st.container(border=True):
        st.markdown("### Document Preview")
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Document / Screenshot", use_column_width=True)
        else:
            st.info(f"Uploaded file: **{uploaded_file.name}** ({uploaded_file.size} bytes). Ready for direct AI visual and textual analysis.")

    if st.button(t["button"], type="primary"):
        if not api_key:
            st.error("No API key available! Please configure your backend key or enter one in the sidebar.")
        else:
            with st.spinner(t["spinner"]):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    suffix = pathlib.Path(uploaded_file.name).suffix
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name

                    gemini_file = client.files.upload(file=tmp_path)

                    prompt = f"""
                    You are Klaro, a compassionate, patient AI family assistant. 
                    A user with low literacy needs help understanding this document type: {mode}. 
                    Read the attached document carefully and explain its core meaning entirely into **{st.session_state.language}**. 
                    Use very basic, everyday words in {st.session_state.language}. Avoid complex jargon.
                    
                    Structure your response clearly using these exact Markdown headers:
                    ### What this document is in plain terms
                    ### Critical things to watch out for (Risks/Deadlines)
                    ### Exact steps the user needs to take next
                    """
                    
                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it",
                        contents=[prompt, gemini_file]
                    )

                    st.success("Analysis complete!")
                    
                    with st.container(border=True):
                        st.markdown("### Klaro's Clear Explanation")
                        st.markdown(response.text)

                    if enable_voice:
                        try:
                            with st.container(border=True):
                                st.markdown("### Native Audio Summary")
                                clean_text = (response.text
                                              .replace("*", "")
                                              .replace("#", ""))
                                
                                lang_code_map = {
                                    "English": "en",
                                    "Spanish": "es",
                                    "Italian": "it",
                                    "French": "fr",
                                    "German": "de",
                                    "Portuguese": "pt",
                                    "Arabic": "ar",
                                    "Japanese": "ja",
                                    "Chinese": "zh-CN"
                                }
                                
                                gtts_lang = lang_code_map.get(st.session_state.language, "en")
                                
                                tts = gTTS(text=clean_text, lang=gtts_lang)
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_tmp:
                                    tts.save(audio_tmp.name)
                                    st.audio(audio_tmp.name, format="audio/mp3")
                        except Exception as audio_err:
                            st.warning(f"Audio generation note: {audio_err}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
