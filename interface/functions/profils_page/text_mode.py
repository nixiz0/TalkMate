import streamlit as st 
from functions.profils_page.rag_system.rag import CustomProcessor
from functions.save_history import profil_save_history
from CONFIG import LANG, PROFILS_SESSION_NAME, PROFILS_HISTORY


def rag_text_files_load(actual_profile, urls, uploaded_files):
    """
    Load and process (vectorize) text files for RAG (Retrieval-Augmented Generation).

    Parameters:
    actual_profile (str): The profile name of the user.
    urls (list): A list of URLs to be processed.
    uploaded_files (list): A list of files uploaded by the user.
    """
    rag = CustomProcessor(actual_profile=actual_profile)
    resources = urls + [file.getvalue() for file in uploaded_files]
    doc_splits = rag.process_ressources(resources)
    rag.process_vectorization(doc_splits)
    st.success("Vectorisation effectuée avec succès !" if LANG == 'fr' else "Vectorization done successfully !")


def rag_text_prompt(actual_profile, question, search_type, session_name=PROFILS_SESSION_NAME, history=PROFILS_HISTORY):
    """
    Process a user's question using RAG and update the session state with the response.

    Parameters:
    actual_profile (str): The profile name of the user.
    question (str): The user's question.
    search_type (str): The type of search to perform.
    session_name (str, optional): The name of the session state variable to update.
    history (str, optional): The directory where history files are stored.
    """
    rag = CustomProcessor(actual_profile=actual_profile)

    # Check if the profile has changed
    if 'previous_profile' in st.session_state and st.session_state['previous_profile'] != actual_profile:
        st.session_state[session_name] = []
        
    # Update the previous profile
    st.session_state['previous_profile'] = actual_profile

    # When user puts their question, start the RAG process
    if question:
        with st.spinner('Traitement' if LANG == 'fr' else 'Processing...'):
            retriever = rag.load_vectorized_documents()
            response, formatted_docs = rag.process_response(retriever, question, search_type)
            
            # Add the question, response, and retrieved documents to the conversation
            st.session_state[session_name].append({"user": question, "assistant": response, "documents": formatted_docs})

            # Display the conversation with an expander for retrieved documents
            for i in range(len(st.session_state[session_name])):
                st.write(f"❓User: {st.session_state[session_name][i]['user']}")
                st.write(f"🤖Assistant: {st.session_state[session_name][i]['assistant']}")
                
                # Use an expander to show retrieved documents only when clicked
                with st.expander("📄 Voir les documents récupérés" if LANG == 'fr' else "📄 View recovered documents"):
                    st.write(st.session_state[session_name][i].get('documents', 'Aucun document récupéré' if LANG == 'fr' else "No documents retrieved"))

            profil_save_history(actual_profile, history, session_name)