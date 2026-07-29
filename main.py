import streamlit as st
from app.core.config import SUPPORTED_LANGUAGES, SUPPORTED_FILE_TYPES
from app.services.translation_service import translate_text
from app.services.tts_service import text_to_speech
from app.services.file_service import extract_text_from_file
from app.utils.helpers import truncate_text, read_audio_bytes

st.set_page_config(page_title="Text Translator & Speech", page_icon="🌐", layout="centered")

st.title("🌐 Text Translator & Text-to-Speech")
st.markdown("Translate text into multiple languages and listen to the audio output.")

# --- Input section ---
st.subheader("1. Provide Input Text")
input_mode = st.radio("Choose input method:", ["Type Text", "Upload File"], horizontal=True)

input_text = ""

if input_mode == "Type Text":
    input_text = st.text_area("Enter text to translate:", height=180, placeholder="Type or paste your text here...")
else:
    uploaded_file = st.file_uploader(
        "Upload a file", type=SUPPORTED_FILE_TYPES,
        help="Supported formats: TXT, PDF, CSV, XLSX"
    )
    if uploaded_file:
        try:
            input_text = extract_text_from_file(uploaded_file)
            st.success(f"File loaded: {uploaded_file.name}")
            st.text_area("Extracted text (preview):", value=input_text[:1000], height=150, disabled=True)
        except Exception as e:
            st.error(f"Failed to read file: {e}")

# --- Language selection ---
st.subheader("2. Select Target Language")
language_name = st.selectbox("Translate to:", list(SUPPORTED_LANGUAGES.keys()), index=8)
language_code = SUPPORTED_LANGUAGES[language_name]

# --- Translate button ---
st.subheader("3. Translate & Generate Audio")
if st.button("Translate", use_container_width=True, type="primary"):
    if not input_text.strip():
        st.warning("Please provide some text before translating.")
    else:
        text_to_translate = truncate_text(input_text)
        with st.spinner("Translating..."):
            try:
                translated = translate_text(text_to_translate, language_name)
                st.session_state["translated_text"] = translated
                st.session_state["language_code"] = language_code
                st.success("Translation complete!")
            except Exception as e:
                st.error(f"Translation failed: {e}")

# --- Show translation & audio ---
if "translated_text" in st.session_state:
    translated = st.session_state["translated_text"]
    lang_code = st.session_state["language_code"]

    st.subheader("Translated Text")
    st.text_area("", value=translated, height=180, disabled=True)

    if st.button("Generate Audio", use_container_width=True):
        with st.spinner("Generating audio..."):
            try:
                audio_path = text_to_speech(translated, lang_code)
                audio_bytes = read_audio_bytes(audio_path)
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    label="Download MP3",
                    data=audio_bytes,
                    file_name="translated_audio.mp3",
                    mime="audio/mp3",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Audio generation failed: {e}")