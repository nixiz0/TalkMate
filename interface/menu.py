import streamlit as st
import base64
from PIL import Image
from io import BytesIO

from CONFIG import LANG
from configuration.choose_lang import get_lang
from configuration.page_title import set_page_title


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

    # Talkmate Presentation
    if LANG == 'fr':
        st.markdown("""
        <div style='text-align: center;'>
            <h2>✨ L'application Talkmate ! ✨</h2>
            <p>Talkmate est une application qui vous permet de :</p>
            <ul style='list-style-type: none;'>
                <li>💬 Parler à des LLMs en local</li>
                <li>🎨 Personnaliser vos interactions</li>
                <li>🔍 Accéder à vos données personnelles via un RAG</li>
                <li>👥 Créer des profils personnalisés par RAG</li>
            </ul>
            <p>Profitez d'une expérience unique et enrichissante avec Talkmate !</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center;'>
            <h2>✨ Talkmate Application ! ✨</h2>
            <p>Talkmate is an application that allows you to:</p>
            <ul style='list-style-type: none;'>
                <li>💬 Chat with local LLMs</li>
                <li>🎨 Customize your interactions</li>
                <li>🔍 Access your personal data via RAG</li>
                <li>👥 Create personalized profiles by RAG</li>
            </ul>
            <p>Enjoy a unique and enriching experience with Talkmate !</p>
        </div>
        """, unsafe_allow_html=True)