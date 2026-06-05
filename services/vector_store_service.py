import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from config.settings import PERSIST_DIRECTORY

# Carrega a base vetorial do disco se existir
def vector_store_load():

    if os.path.exists(PERSIST_DIRECTORY):

        return Chroma(
            persist_directory= PERSIST_DIRECTORY,
            embedding_function= OpenAIEmbeddings(),
        )
    
    return None


# Adiciona chunks à base existente ou cria uma nova
def vector_store_save_documents(chunks, vector_store = None):

    if vector_store:

        vector_store.add_documents(chunks)

        return vector_store
    
    return Chroma.from_documents(
        documents= chunks,
        embedding= OpenAIEmbeddings(),
        persist_directory= PERSIST_DIRECTORY,
    )