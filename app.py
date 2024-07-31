import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
with st.sidebar:
    speech_key = st.text_input("Azure OpenAI Key", key="chatbot_api_key", type="password")
    service_region = st.text_input("region service", key="region_service", type="password")
   
# load_dotenv()
# speech_key = os.getenv('AZURE_SPEECH_KEY')
# service_region = os.getenv('AZURE_SPEECH_REGION')
# speech_key = st.secrets["speech_service"]["key"]
# service_region = st.secrets["speech_service"]["region"]

# Define language codes
lang_codes = {
    'Arabic': 'ar-EG', 'Bahasa Indonesian': 'id-ID',
    'Chinese Mandarin': 'zh-CN', 'Dutch': 'nl-NL', 'English (default)': 'en-US', 
    'French': 'fr-FR', 'German': 'de-DE', 'Hindi': 'hi-IN', 'Italian': 'it-IT', 
    'Japanese': 'ja-JP', 'Korean': 'ko-KR', 'Russian': 'ru-RU', 'Spanish': 'es-ES', 
    
}
your_lang = {
    'Arabic': 'ar', 'Bahasa Indonesian': 'id',
    'Chinese Mandarin': 'lzh', 'Dutch': 'nl', 'English (default)': 'en', 
    'French': 'fr', 'German': 'de', 'Hindi': 'hi', 'Italian': 'it', 
    'Japanese': 'ja', 'Korean': 'ko', 'Russian': 'ru', 'Spanish': 'es', 
    
}

st.sidebar.title("Multilingual Speech Translation")

# Sidebar for language selection
lang = st.sidebar.selectbox('Choose your language', list(lang_codes.keys()), index=5)
lang_tr = st.sidebar.selectbox('Translate to', list(your_lang.keys()), index=6)

recognition_lang_code = lang_codes[lang]
translation_lang_code = your_lang[lang_tr]

def recognize_from_microphone(recognition_lang_code, translation_lang_code):
    try:
        # Configure the translation
        speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=speech_key, region=service_region)
        speech_translation_config.speech_recognition_language = recognition_lang_code
        speech_translation_config.add_target_language(translation_lang_code)

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        translation_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=speech_translation_config, audio_config=audio_config
        )

        st.info("Speak into your microphone 🗣️...", icon="💡")
        with st.spinner("Listening..."):
            translation_recognition_result = translation_recognizer.recognize_once_async().get()

            if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
                st.subheader("Translation")
                st.success(f"Translated into '{translation_lang_code}': {translation_recognition_result.translations[translation_lang_code]}")
            elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                st.error(f"No speech could be recognized: {translation_recognition_result.no_match_details}")
            elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = translation_recognition_result.cancellation_details
                st.error(f"Speech Recognition canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    st.error(f"Error details: {cancellation_details.error_details}")
                    st.error("Did you set the speech resource key and region values?")

            # Set up speech synthesis
            speech_synthesis_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            voice_name = "en-US-JennyMultilingualNeural"  # Default to English
            if translation_lang_code == "id":
                voice_name = "id-ID-ArdiNeural"
            speech_synthesis_config.speech_synthesis_voice_name = voice_name
            
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_synthesis_config)

            # Synthesize the recognized text
            text = translation_recognition_result.translations[translation_lang_code]
            result = speech_synthesizer.speak_text_async(text).get()

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Button to trigger translation
if st.button("Start translation"):
    recognize_from_microphone(recognition_lang_code, translation_lang_code)
