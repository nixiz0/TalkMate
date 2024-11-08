import streamlit as st 
from functions.profils_page.rag_system.rag import CustomProcessor
from functions.save_history import profil_save_history
from CONFIG import LANG, PROFILS_SESSION_NAME, PROFILS_HISTORY


def rag_text_files_load(urls, uploaded_files):
    rag = CustomProcessor()
    resources = urls + [file.getvalue() for file in uploaded_files]
    doc_splits = rag.process_ressources(resources)
    rag.process_vectorization(doc_splits)
    st.success("Vectorisation effectuée avec succès !" if LANG == 'fr' else "Vectorization done successfully !")

def rag_text_prompt(question, actual_profile):
    rag = CustomProcessor()

    # Check if the profile has changed
    if 'previous_profile' in st.session_state and st.session_state['previous_profile'] != actual_profile:
        st.session_state[PROFILS_SESSION_NAME] = []
        
    # Update the previous profile
    st.session_state['previous_profile'] = actual_profile

    # When user puts their question, start the RAG process
    if question:
        with st.spinner('Traitement' if LANG == 'fr' else 'Processing...'):
            retriever = rag.load_vectorized_documents()
            response, formatted_docs = rag.process_response(retriever, question)
            
            # Add the question, response, and retrieved documents to the conversation
            st.session_state[PROFILS_SESSION_NAME].append({"user": question, "assistant": response, "documents": formatted_docs})

            # Display the conversation with an expander for retrieved documents
            for i in range(len(st.session_state[PROFILS_SESSION_NAME])):
                st.write(f"❓User: {st.session_state[PROFILS_SESSION_NAME][i]['user']}")
                st.write(f"🤖Assistant: {st.session_state[PROFILS_SESSION_NAME][i]['assistant']}")
                
                # Use an expander to show retrieved documents only when clicked
                with st.expander("📄 Voir les documents récupérés" if LANG == 'fr' else "📄 View recovered documents"):
                    st.write(st.session_state[PROFILS_SESSION_NAME][i].get('documents', 'Aucun document récupéré' if LANG == 'fr' else "No documents retrieved"))

            profil_save_history(PROFILS_HISTORY, actual_profile, PROFILS_SESSION_NAME)