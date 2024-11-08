import streamlit as st 
from CONFIG import LANG, PROFILS_SEARCH_TYPE, AUDIO_TRANSCRIPTION_PATH
from functions.profils_page.rag_system.rag import CustomProcessor
from functions.save_history import profil_save_history
from speech_to_text.record import record_audio
from speech_to_text.speech import SpeechToText
from voice.voice_system import NarratorVoice


class RAG_Discussion():
    def __init__(self, lang, llm_model, embeddings_model, question, micro_index, actual_profile, history_dir, session_name):
        self.lang = lang
        self.llm_model = llm_model
        self.embeddings_model = embeddings_model
        self.question = question
        self.micro_index = micro_index
        self.actual_profile = actual_profile
        self.history_dir = history_dir
        self.session_name = session_name

    def rag_discussion_prompt(self):
        rag = CustomProcessor(language=self.lang, llm_model=self.llm_model, embeddings_model=self.embeddings_model, actual_profile=self.actual_profile)

        # Check if the profile has changed
        if 'previous_profile' in st.session_state and st.session_state['previous_profile'] != self.actual_profile:
            st.session_state[self.session_name] = []

        # Update the previous profile
        st.session_state['previous_profile'] = self.actual_profile

        if st.sidebar.button('🎙️ Mode Discussion' if self.lang == 'fr' else '🎙️ Discussion Mode'):
            if self.lang == "fr":
                st.sidebar.info("Écoute..")
            else: 
                st.sidebar.info("Listen..")

            # Recording audio
            record_audio(filename=AUDIO_TRANSCRIPTION_PATH, device_index=self.micro_index, rate=44100, chunk=1024, threshold=200, pre_recording_buffer_length=2)

            if self.lang == "fr":
                st.sidebar.warning("Transcription en cours..")
            else: 
                st.sidebar.warning("Transcription in progress..")

            # Transcription Speech To Text
            speech = SpeechToText()
            text = speech.transcribe(AUDIO_TRANSCRIPTION_PATH)
            
            question = text
            
            if self.lang == "fr":
                st.sidebar.success("Transcription terminée")
            else: 
                st.sidebar.success("Transcription completed")

            # When user put his question start the RAG
            if question:
                with st.spinner('Processing...'):
                    retriever = rag.load_vectorized_documents()
                    response, formatted_docs = rag.process_response(retriever, question, PROFILS_SEARCH_TYPE)

                    # Add the question, response, and retrieved documents to the conversation
                    st.session_state[self.session_name].append({"user": question, "assistant": response, "documents": formatted_docs})

                    # Display the conversation with an expander for retrieved documents
                    for i in range(len(st.session_state[self.session_name])):
                        st.write(f"❓User: {st.session_state[self.session_name][i]['user']}")
                        st.write(f"🤖Assistant: {st.session_state[self.session_name][i]['assistant']}")
                        
                        # Use an expander to show retrieved documents only when clicked
                        with st.expander("📄 Voir les documents récupérés" if LANG == 'fr' else "📄 View recovered documents"):
                            st.write(st.session_state[self.session_name][i].get('documents', 'Aucun document récupéré' if LANG == 'fr' else "No documents retrieved"))

                    profil_save_history(self.actual_profile, self.history_dir, self.session_name)

                    # Use NarratorVoice to speak the response
                    narrator = NarratorVoice()
                    narrator.speak(response)