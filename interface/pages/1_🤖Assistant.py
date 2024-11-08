import streamlit as st
import os

from CONFIG import LANG, ASSISTANT_LLM, ASSISTANT_SESSION_NAME, ASSISTANT_HISTORY_DIR
from configuration.choose_llm import view_install_llms, get_llm
from configuration.page_title import set_page_title
from functions.assistant_page.build_custom_llm import custom_llm
from functions.assistant_page.text_mode import text_prompt


# ---[Page Title]---
set_page_title("🤖 Assistant")

# ---[Configuration Initialization]---
if not os.path.exists(ASSISTANT_HISTORY_DIR):
    os.makedirs(ASSISTANT_HISTORY_DIR)

if ASSISTANT_SESSION_NAME not in st.session_state:
    st.session_state[ASSISTANT_SESSION_NAME] = []

session_state_updated = st.session_state[ASSISTANT_SESSION_NAME]
if 'model_use' not in st.session_state:
    st.session_state.model_use = ""


# ---[Sidebar Code]---
# Add a radio button to enable configuration mode
config_mode = st.sidebar.checkbox("⚙️Configuration")
if config_mode:
    model_names = view_install_llms()
    model_names.insert(0, "")
    model_use = st.sidebar.selectbox('🔬 Modèles' if LANG == "fr" else '🔬 Models', model_names, index=model_names.index(st.session_state.model_use) if st.session_state.model_use in model_names else 0)
    
    if model_use:
        get_llm('ASSISTANT_LLM', model_use)
        custom_llm(model_use)

    if not model_use:
        st.sidebar.warning("Veuillez choisir un modèle" if LANG == 'fr' else "Please choose a model")

st.sidebar.markdown("<hr style='margin:0px;'>", unsafe_allow_html=True)


# ---[Page Code]---
# Add a picker to choose a chat history file
history_files = os.listdir(ASSISTANT_HISTORY_DIR)
selected_file = st.sidebar.selectbox("Historique de conversation" if LANG == 'fr' else 
                                     "Conversation history file", [""] + history_files)

prompt = st.chat_input("Posez une question" if LANG == 'fr' else "Ask a Question")

text_prompt(prompt, LANG, ASSISTANT_LLM, session_state_updated, selected_file, ASSISTANT_HISTORY_DIR, ASSISTANT_SESSION_NAME)

# Show all previous posts
for message in st.session_state[ASSISTANT_SESSION_NAME]:
    with st.chat_message(message["role"]):
        st.write(message["content"])