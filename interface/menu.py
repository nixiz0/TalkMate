import streamlit as st
import base64
from PIL import Image
from io import BytesIO

from CONFIG import LANG
from configuration.choose_lang import get_lang
from configuration.page_title import set_page_title
from speech_to_text.micro import select_microphone
from voice.voice_system import NarratorVoice


# ---[Page Title]---
set_page_title("Menu TalkMate")

# ---[Sidebar Code]---
# Add dropdown list to sidebar
lang_choice = st.sidebar.selectbox(
    '🔤Language',
    ('', 'English', 'French'),
)

# Update the LANG variable according to the user's choice
if lang_choice == 'French':
    get_lang('fr')
elif lang_choice == 'English':
    get_lang('en')

select_microphone(LANG)
voice_index = NarratorVoice()
voice_index.select_voice(LANG)

# Instantiate voice_id and device_index sessions in the app
voice_id = st.session_state['selected_voice_id']
micro_index = st.session_state['selected_device_index']

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)


# ---[Page Code]---
# Create three columns with different proportions
col1, col2, col3 = st.columns([2,50,2])

# Use the middle column for your elements
with col2:
    # Open image & Convert to base64 to display in markdown
    user_logo = Image.open('./interface/ressources/user-icon.png')
    buffered = BytesIO()
    user_logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Show image centered with a defined width
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_str}' width='250'/></div>", unsafe_allow_html=True)

    # Welcome Title
    if LANG == 'fr':
        st.markdown("<h1 style='text-align: center;'>Bienvenue cher Utilisateur</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center;'>Welcom dear User</h1>", unsafe_allow_html=True)

    # H2 app name title
    if LANG == 'fr':
        st.markdown("<h2 style='text-align: center;'>sur TalkMate</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center;'>in TalkMate</h2>", unsafe_allow_html=True)

    # Text Presentation
    if LANG == 'fr':
        st.markdown("<p style='text-align: center;'> \
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. \
                    Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. \
                    </p>", 
                    unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align: center;'> \
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                    Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. \
                    Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. \
                    </p>", 
                    unsafe_allow_html=True)