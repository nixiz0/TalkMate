import streamlit as st 
import json 
import os
import ollama
from CONFIG import AUDIO_TRANSCRIPTION_PATH
from functions.save_history import assistant_save_history
from speech_to_text.record import record_audio
from speech_to_text.speech import SpeechToText
from voice.voice_system import NarratorVoice


def process_discussion(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name):
    """
    Process a discussion by recording audio, transcribing it, and generating a response using a language model.

    Parameters:
    lang (str): The language for the UI elements.
    model_use (str): The language model to use.
    micro_index (int): The index of the microphone to use.
    session_state_updated (list): The updated session state containing chat history.
    selected_file (str): The currently selected file name.
    history_dir (str): The directory where history files are stored.
    session_name (str): The name of the session state variable to update.

    Returns:
    list: The updated session state containing chat history.
    """
    if lang == "fr":
        st.sidebar.info("Écoute..")
    else: 
        st.sidebar.info("Listen..")

    # Recording audio
    record_audio(filename=AUDIO_TRANSCRIPTION_PATH, device_index=micro_index, rate=44100, chunk=1024, threshold=200, pre_recording_buffer_length=2)

    if lang == "fr":
        st.sidebar.warning("Transcription en cours..")
    else: 
        st.sidebar.warning("Transcription in progress..")

    # Transcription Speech To Text
    speech = SpeechToText()
    text = speech.transcribe(AUDIO_TRANSCRIPTION_PATH)

    # Add user prompt to session updated
    session_state_updated.append({
        "role": "user",
        "content": text,
    })

    if lang == "fr":
        st.sidebar.success("Transcription terminée")
    else: 
        st.sidebar.success("Transcription completed")

    # Push the user prompt in the LLM model and return response
    with st.spinner("Réflexion.." if lang == 'fr' else "Thinking.."):
        result = ollama.chat(model=model_use, messages=session_state_updated)
        response = result["message"]["content"]

        # Add model response to message list
        session_state_updated.append({
            "role": "assistant",
            "content": response,
        })

    if lang == "fr":
        st.sidebar.success("Réponse de l'assistant obtenue")
    else: 
        st.sidebar.success("Assistant response received")

    # Show all previous posts
    for message in st.session_state[session_name]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Use NarratorVoice to speak the response
    narrator = NarratorVoice()
    narrator.speak(response)

    # Save in new json file if first prompt or an already existing json and add updated prompt
    selected_file = assistant_save_history(session_state_updated, selected_file, history_dir, session_name)

    return session_state_updated


def discussion_prompt(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name):  
    """
    Handle the discussion prompt, manage session state, and process the discussion.

    Parameters:
    lang (str): The language for the UI elements.
    model_use (str): The language model to use.
    micro_index (int): The index of the microphone to use.
    session_state_updated (list): The updated session state containing chat history.
    selected_file (str): The currently selected file name.
    history_dir (str): The directory where history files are stored.
    session_name (str): The name of the session state variable to update.

    Returns:
    list: The updated session state containing chat history.
    """
    
    # Recover json load file if the user select and load a json
    if selected_file:
        with open(os.path.join(history_dir, selected_file), "r", encoding="utf8") as f:
            st.session_state[session_name] = json.load(f)

    continue_discussion = st.session_state['continue_discussion']
    if continue_discussion == False:
        if st.sidebar.button('🎙️ Mode Discussion' if lang == 'fr' else '🎙️ Discussion Mode'):
            return process_discussion(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name)
    else: 
        stop_button = st.sidebar.button('Stop')
        while not stop_button:
            session_state_updated = process_discussion(lang, model_use, micro_index, session_state_updated, selected_file, history_dir, session_name)
            # Update the stop button status at the end of each loop
            stop_button = st.sidebar.button('Stop')

        return session_state_updated