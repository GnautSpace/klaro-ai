Markdown
# Klaro AI

> Turn confusing legal contracts, scary medical prescriptions, and messy government bills into simple, clear native language—complete with native voice playback!

Hey! Built this for everyone who has ever stared at a 10-page terms-of-service document or a medical bill and thought, *"I have zero idea what any of this means."* 

Klaro AI acts like a patient, compassionate family assistant that reads documents for you, breaks them down into plain words, and reads them back out loud in your native accent.

---

## What it does
* **Scans Docs Instantly:** Drop in a PDF, image, scan, or WhatsApp screenshot. It handles messy formatting and scanned files natively using the Google GenAI File API.
* **Dynamic UI Translation:** Uses Gemma to translate the whole app interface into whatever language you pick on the fly.
* **Native Voice Playback:** Reads the plain-language explanation back to you with the correct native accent (Spanish, Hindi, French, German, and more) using `gTTS`.
* **Bring Your Own Key:** Simple sidebar config so users can plug in their own Google GenAI API key.

---

## Tech Stack
* **Frontend/UI:** [Streamlit](https://streamlit.io/),[Render](https://render.com)
* **AI Engine:** Google GenAI SDK (`google-genai`) powered by Gemma models
* **Audio:** `gTTS` (Google Text-to-Speech) for native accents
* **File Handling:** Python `tempfile` & `pathlib`

---

## How to Run It Locally

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/your-username/klaro-ai.git](https://github.com/your-username/klaro-ai.git)
   cd klaro-ai
   ```

2. Install the dependencies:
   ```bash
    pip install streamlit google-genai pillow pypdf gTTS
   ```

3. Fire up the app:
   ```bash
   streamlit run app.py
   ```

4. Add your key-> Grab a free key from Google AI Studio, paste it into the sidebar, upload a confusing document, and let Klaro do the rest (^_^)v