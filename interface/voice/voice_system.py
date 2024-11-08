import streamlit as st
import pyttsx3
import re


def split_text_and_code(text):
    # Define a regex pattern for code detection
    pattern = r'(```.*?```)'  # This pattern matches text within triple backticks
    
    # Use regex split to separate text and code
    segments = re.split(pattern, text, flags=re.DOTALL)
    
    return segments

class NarratorVoice:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()

    def get_voice_list(self):
        voices = self.engine.getProperty('voices')
        voice_dict = {i: voice for i, voice in enumerate(voices)}
        return voice_dict

    def select_voice(self, language):
        voices = self.get_voice_list()
        voice_names = [voices[i].name for i in voices]

        if 'selected_voice_id' not in st.session_state:
            st.session_state['selected_voice_id'] = voices[0].id 

        if language == "fr":
            selected_voice_name = st.sidebar.selectbox('Sélectionnez la voix synthétique à utiliser', voice_names, index=voice_names.index([voice.name for voice in voices.values() if voice.id == st.session_state['selected_voice_id']][0]))
        else:
            selected_voice_name = st.sidebar.selectbox('Select the synthetic voice to use', voice_names, index=voice_names.index([voice.name for voice in voices.values() if voice.id == st.session_state['selected_voice_id']][0]))

        st.session_state['selected_voice_id'] = [voice.id for voice in voices.values() if voice.name == selected_voice_name][0]
        return st.session_state['selected_voice_id'] 
        
    def speak(self, text):
        # Split the text into text and code segments
        segments = split_text_and_code(text)
        
        for segment in segments:
            # Check if the segment is code
            if segment.startswith('```') and segment.endswith('```'):
                print("Code detected, not reading out loud.")
            else:
                voice = st.session_state.get('selected_voice_id', None)
                
                # Set narrator voice
                self.engine.setProperty('voice', voice)

                # Convert text to speech
                self.engine.say(segment)

                # Wait for any pending speech to complete
                self.engine.runAndWait()