import os
import shutil
import tempfile
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from CONFIG import LANG, PROFILS_LLM, PROFILS_EMBEDDING_LLM, PROFILS_BASE_DIR, PROFILS_DEFAULT_PROFIL, \
                   PROFILS_CHUNKS, PROFILS_OVERLAP, PROFILS_SIMILARITY, PROFILS_DOCUMENTS


class CustomProcessor:
    def __init__(self, language=LANG, llm_model=PROFILS_LLM, embeddings_model=PROFILS_EMBEDDING_LLM, base_dir=PROFILS_BASE_DIR, actual_profile=PROFILS_DEFAULT_PROFIL, 
                 chunks=PROFILS_CHUNKS, overlap=PROFILS_OVERLAP, similarity=PROFILS_SIMILARITY, documents=PROFILS_DOCUMENTS):
        self.language = language
        self.llm_model = llm_model
        self.embeddings_model = embeddings_model
        self.base_dir = base_dir
        self.actual_profile = actual_profile
        self.chunks = chunks
        self.overlap = overlap
        self.similarity = similarity
        self.documents = documents

        self.db_dir = os.path.join(self.base_dir, self.actual_profile)
        os.makedirs(self.db_dir, exist_ok=True)

    def process_ressources(self, resources):
        docs = []
        for resource in resources:
            if isinstance(resource, str):
                if resource.startswith("http"):
                    if resource.lower().endswith('.pdf'):
                        loader = PyPDFLoader(resource)
                    else:
                        loader = WebBaseLoader(resource)
                    docs.extend(loader.load())
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(resource)
                    temp_file_path = temp_file.name
                docs.extend(PyPDFLoader(temp_file_path).load())
                os.unlink(temp_file_path)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunks, chunk_overlap=self.overlap)
        doc_splits = text_splitter.split_documents(docs)
        return doc_splits
    
    def process_vectorization(self, doc_splits):
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name=self.actual_profile,
            embedding=OllamaEmbeddings(model=self.embeddings_model),
            persist_directory=self.db_dir,
        )
        return vectorstore.as_retriever()

    def process_response(self, retriever, question, search_type):
        if search_type == "similarity_score_threshold":
            retriever = retriever.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={'score_threshold': self.similarity, 'k': self.documents}
            )
        elif search_type == "mmr":
            retriever = retriever.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={'fetch_k': 20, 'lambda_mult': 0.5, 'k': self.documents}
            )
        elif search_type == "similarity":
            retriever = retriever.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={'k': self.documents}
            )
        else:
            raise ValueError(f"Unknown search_type: {search_type}")

        model_local = OllamaLLM(model=self.llm_model)
        after_rag_template = """Répond à la question en français en te basant uniquement sur le contexte suivant:
        Contexte: {context}
        Question: {question}
        """ if self.language == "Fr" else """Answer to the question in english based only on the following context:
        Context: {context}
        Question: {question}
        """

        after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
        after_rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | after_rag_prompt
            | model_local
            | StrOutputParser()
        )
        
        retrieved_docs = retriever.invoke(question)
        formatted_docs = "\n\n".join([f"Document {i+1}: {doc.page_content}" for i, doc in enumerate(retrieved_docs)])
        
        response = after_rag_chain.invoke(question)
        
        return response, formatted_docs
        
    def load_vectorized_documents(self):        
        vectorstore = Chroma(
            collection_name=self.actual_profile,
            embedding_function=OllamaEmbeddings(model=self.embeddings_model),
            persist_directory=self.db_dir
        )
        return vectorstore.as_retriever()
    
    def delete_profile(self):
        if os.path.exists(self.db_dir):
            shutil.rmtree(self.db_dir)