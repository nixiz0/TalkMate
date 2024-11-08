LANG = 'fr'

ASSISTANT_LLM = 'llama3.1:latest'
ASSISTANT_SESSION_NAME = "assistant_state"
ASSISTANT_HISTORY_DIR = "conversation/assistant_history"

PROFILS_LLM = 'llama3.1:latest'
PROFILS_EMBEDDING_LLM = 'nomic-embed-text:latest'
PROFILS_SESSION_NAME = "profils_state"
PROFILS_HISTORY = "conversation/profils_history"
PROFILS_BASE_DIR = "conversation/user_profils"
PROFILS_DEFAULT_PROFIL = "default_profil"
PROFILS_SEARCH_TYPE = "similarity"
PROFILS_CHUNKS = 1500
PROFILS_OVERLAP = 100
PROFILS_FETCH_K = 20
PROFILS_LAMBDA_MULT = 0.5
PROFILS_SIMILARITY = 0.6
PROFILS_DOCUMENTS = 4


# [Speech to Text Config]
AUDIO_TRANSCRIPTION_PATH = "interface/speech_to_text/temp_audio/audio.wav"