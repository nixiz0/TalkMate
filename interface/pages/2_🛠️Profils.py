import streamlit as st
import json 
import os
import unicodedata
import re

from CONFIG import *
from configuration.choose_llm import view_install_llms, get_llm
from configuration.rag_config import get_rag_config_values, rag_search_type, rag_chunks, rag_fetch_k_lambda_mult, rag_similarity, rag_documents
from configuration.page_title import set_page_title
from functions.app_button import AppButton
from functions.profils_page.rag_system.rag import CustomProcessor
from functions.profils_page.text_mode import rag_text_files_load, rag_text_prompt


# ---[Page Title]---
set_page_title("🛠️ Question")

# ---[Configuration Initialization]---
load_vectorize = None
question = None

if not os.path.exists(PROFILS_BASE_DIR):
    os.makedirs(PROFILS_BASE_DIR)

if PROFILS_SESSION_NAME not in st.session_state:
    st.session_state[PROFILS_SESSION_NAME] = []


# ---[Sidebar Code]---
# Checkbox to view all config
config_mode = st.sidebar.checkbox("⚙️Configuration")
if config_mode:
    model_names = view_install_llms()
    model_names.insert(0, "")
    model_use = st.sidebar.selectbox('🔬 Modèles' if LANG == "fr" else '🔬 Models', model_names)
    if model_use:
        get_llm('PROFILS_LLM', model_use)
    if not model_use:
        st.sidebar.warning("Veuillez choisir un modèle" if LANG == 'fr' else "Please choose a model")

    model_embed_names = view_install_llms()
    model_embed_names.insert(0, "")
    embeddings_model = st.sidebar.selectbox("Modèles Embeddings" if LANG == "fr" else "Embeddings Models", model_embed_names)
    if embeddings_model:
        get_llm('PROFILS_EMBEDDING_LLM', embeddings_model)
    if not embeddings_model:
        st.sidebar.warning("Veuillez choisir un modèle d'embedding" if LANG == 'fr' else "Please choose an embedding model")

    config_values = get_rag_config_values()

    search_types = ["similarity", "mmr", "similarity_score_threshold"]
    search_type_index = search_types.index(PROFILS_SEARCH_TYPE) if PROFILS_SEARCH_TYPE in search_types else 0
    search_type = st.sidebar.selectbox('🔍 Type de recherche' if LANG == "fr" else '🔍 Search Type', search_types, index=search_type_index)
    rag_search_type(search_type)

    chunk_size = st.sidebar.number_input('Taille des Chunks' if LANG == 'fr' else "Chunks Size", 100, 10000, config_values['PROFILS_CHUNKS'], 100)
    chunk_overlap = st.sidebar.number_input('Chevauchement' if LANG == 'fr' else "Overlap", 20, 1000, config_values['PROFILS_OVERLAP'], 10)
    rag_chunks(chunk_size, chunk_overlap)

    if search_type == "similarity_score_threshold":
        similarity_threshold = st.sidebar.slider('Seuil de similarité' if LANG == 'fr' else "Similarity Threshold", 0.1, 1.0, config_values['PROFILS_SIMILARITY'], 0.05)
        rag_similarity(similarity_threshold)

    if search_type == "mmr":
        fetch_k = st.sidebar.number_input('Fetch k', 1, 100, config_values['PROFILS_FETCH_K'], 1)
        lambda_mult = st.sidebar.slider('Lambda Mult', 0.0, 1.0, config_values['PROFILS_LAMBDA_MULT'], 0.1)
        rag_fetch_k_lambda_mult(fetch_k, lambda_mult)

    num_documents = st.sidebar.slider('Nombre de documents' if LANG == 'fr' else "Number of documents", 1, 20, config_values['PROFILS_DOCUMENTS'], 1)
    rag_documents(num_documents)

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Retrieve all folders (profils) & Add default profil to list if doesn't already exist
profiles = [name for name in os.listdir(PROFILS_BASE_DIR) if os.path.isdir(os.path.join(PROFILS_BASE_DIR, name)) 
            and name not in ['__pycache__', 'temp-file']]
profiles.insert(0, '')
if PROFILS_DEFAULT_PROFIL not in profiles:
    profiles.insert(1, PROFILS_DEFAULT_PROFIL)

# Profile Selector
actual_profile = st.sidebar.selectbox("Sélectionnez un profil" if LANG == 'fr' else "Select a profil", profiles)
if actual_profile == '':
    # Input for the name of a new profil if the user want
    new_profile_name = st.sidebar.text_input("Entrez le nom du nouveau profil" if LANG == 'fr' else "Enter the name of the new profile")
    if not new_profile_name == '':
        # Remove accents & punctuations (except underscore) & Replace spaces with underscores
        new_profile_name = unicodedata.normalize('NFD', new_profile_name).encode('ascii', 'ignore').decode("utf-8")
        new_profile_name = re.sub(r'[^\w\s]', '', new_profile_name)
        new_profile_name = new_profile_name.replace(' ', '_')

        # Button to create the new profile
        if st.sidebar.button("Créer" if LANG == 'fr' else "Create"):
            new_profile_path = os.path.join(PROFILS_BASE_DIR, new_profile_name)
            if not os.path.exists(new_profile_path):
                os.makedirs(new_profile_path)
                st.rerun()
            else:
                st.sidebar.error(f"Le profil {new_profile_name} existe déjà." if LANG == 'fr' else f"The {new_profile_name} profile already exists.")

if not actual_profile == '':
    # Button to delete current profile
    if st.sidebar.button("Supprimer profil actuel" if LANG == 'fr' else "Delete actual profil"):
        try:
            rag = CustomProcessor(actual_profile=actual_profile)
            rag.delete_profile()
            st.rerun()
        except Exception as e:
            st.error("Veuillez redémarrer l\'application pour supprimer correctement le profil." if LANG == 'fr' else 
                     "Please restart the application to delete the profile correctly.")
        
    st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)
        
    load_vectorize = st.sidebar.checkbox("Base de donnée actuelle" if LANG == 'fr' else "Current Database")

st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)

# Add a picker to choose a chat history file
if not os.path.exists(PROFILS_HISTORY):
    os.makedirs(PROFILS_HISTORY)
history_files = os.listdir(PROFILS_HISTORY)
selected_file = st.sidebar.selectbox("Historique des conversations" if LANG == 'fr' else 
                                     "Conversation history files", [""] + history_files)

# Load the selected conversation
if selected_file:
    st.session_state[PROFILS_SESSION_NAME] = []
    with open(f'{PROFILS_HISTORY}/{selected_file}', 'r', encoding="utf8") as f:
        loaded_conversation = json.load(f)
        # Display the loaded conversation
        for i in range(len(loaded_conversation)):
            st.write(f"❓User: {loaded_conversation[i]['user']}")
            st.write(f"🤖Assistant: {loaded_conversation[i]['assistant']}")

    rag_app_btn = AppButton(LANG, PROFILS_HISTORY, selected_file)
    rag_app_btn.rename_file()
    rag_app_btn.download_as_csv()
    rag_app_btn.delete_file()


# ---[Page Code]---
if not selected_file:
    # Set messages in different languages
    messages = {
        "fr": {
            "title": "Assistant sur vos Données",
            "url_text": "Entrez les URL ici (une par ligne):",
            "file_uploader_text": "Choisissez vos fichiers à traiter",
        },
        "en": {
            "title": "Assistant to your Data",
            "url_text": "Enter the URL here (one per line):",
            "file_uploader_text": "Choose your files to process",
        }
    }

    # Use messages according to the chosen language
    lang_messages = messages.get(LANG, messages["en"])

    if load_vectorize == False:
        # Show UI elements with corresponding messages
        st.title(lang_messages["title"])
        urls = st.text_area(lang_messages["url_text"])
        urls = urls.split("\n")

        # Upload PDF
        uploaded_files = st.file_uploader(lang_messages["file_uploader_text"], type=["pdf"], accept_multiple_files=True)
        if not uploaded_files and not urls[0]:
            st.warning("Veuillez rentrer au moins une ressource à traiter" if LANG == 'fr' else 
                       "Please enter at least one resource to process")
        else:
            if PROFILS_LLM and PROFILS_EMBEDDING_LLM:
                if st.button("Vectoriser" if LANG == 'fr' else "Vectorize"):
                    # RAG Text add Documents (vectorize)
                    rag_text_files_load(actual_profile, urls, uploaded_files)

    elif load_vectorize == True: 
        question = st.chat_input("Entrez votre question ici :" if LANG == 'fr' else "Enter your question here :")
        if question == None: 
            st.sidebar.warning("Veuillez saisir une question" if LANG == "fr" else "Please enter a question")
        else: 
            # RAG Text
            rag_text_prompt(actual_profile, question, PROFILS_SEARCH_TYPE)

    else:
        st.warning("Veuillez choisir ou créer un profile" if LANG == 'fr' else "Please choose or create a profile")

    st.sidebar.markdown("<hr style='margin:5px;'>", unsafe_allow_html=True)